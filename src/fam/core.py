from pathlib import Path
import subprocess
from fam import filename
from fam.cli import app_cli
from fam.utils import fprint


def check_for_update() -> None:
    """
    Callback to check for updates before executing any command.
    Only checks once and informs the user if updates are available.
    """

    update_file: Path = Path(app_cli.directory.app_dir) / filename.UPDATE

    if update_file.exists():
        return  # Skip if the update check has already been done

    try:
        # Fetch the latest changes from the remote repository
        subprocess.run(["git", "fetch"], check=True, capture_output=True)

        # Check if the local branch is behind the remote branch
        result = subprocess.run(
            ["git", "status", "-uno"], check=True, capture_output=True, text=True
        )

        if "Your branch is behind" in result.stdout:
            fprint(
                "Updates are available. Please run the 'upgrade' command to update the project."
            )
            update_file.touch()

    except subprocess.CalledProcessError as e:
        fprint(f"Error checking for updates: {e}")
