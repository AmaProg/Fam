from pathlib import Path
import subprocess

from alembic.config import Config
from alembic import command
from alembic.script import ScriptDirectory

from fam import filename
from fam.utils import fprint, fprint_panel
from fam.cli import app_cli


class Update:
    def __init__(self) -> None:
        pass

    def install_new_version(self) -> bool:
        """
        Upgrade the project by pulling the latest changes from the Git repository.
        """

        update_file: Path = Path(app_cli.directory.app_dir) / filename.UPDATE

        try:
            # Fetch the latest changes from the remote repository
            self._fetch_repository()

            if self._is_local_branch_behind():

                self._pull_version()

                fprint("Project successfully upgraded.")

                # Remove the update check file to allow future checks
                if update_file.exists():
                    update_file.unlink()

                return True

            else:
                fprint("Your project is up-to-date.")
                return True

        except subprocess.CalledProcessError as e:
            fprint(f"Error during upgrade: {e}")
            return False

    def check_new_version(self) -> None:
        """
        Callback to check for updates before executing any command.
        Only checks once and informs the user if updates are available.
        """

        update_file: Path = Path(app_cli.directory.app_dir) / filename.UPDATE

        if update_file.exists():
            return  # Skip if the update check has already been done

        try:
            # Fetch the latest changes from the remote repository
            self._fetch_repository()

            # Check if the local branch is behind the remote branch
            if self._is_local_branch_behind():
                msg: str = (
                    "A new update is now available. Please use the 'upgrade' command to update the application for all users."
                )
                fprint_panel(msg=msg, title="New Update")

                update_file.touch()

        except subprocess.CalledProcessError as e:
            fprint(f"Error checking for updates: {e}")

    def apply_database_migrations(self, database_url: str) -> None:

        alembic_cfg = Config("alembic_users.ini")
        alembic_cfg.set_main_option("user_database_url", database_url)
        alembic_cfg.set_main_option("is_user", "True")
        alembic_cfg.set_main_option("script_location", "alembic/users")

        script = ScriptDirectory.from_config(alembic_cfg)
        latest_script = script.get_current_head()
        current_revision = latest_script

        if current_revision is not None:
            command.upgrade(alembic_cfg, current_revision)

    def _fetch_repository(self) -> None:
        # Fetch the latest changes from the remote repository
        command: list[str] = ["git", "fetch"]

        subprocess.run(command, check=True, capture_output=True)

    def _is_local_branch_behind(self) -> bool:

        # Check if the local branch is behind the remote branch
        command: list[str] = ["git", "status", "-uno"]

        result = subprocess.run(command, check=True, capture_output=True, text=True)

        return True if "Your branch is behind" in result.stdout else False

    def _pull_version(self) -> None:

        comamnd: list[str] = ["git", "pull", "origin", "main"]

        subprocess.run(comamnd, check=True, capture_output=True)
