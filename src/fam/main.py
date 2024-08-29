from pathlib import Path
import subprocess
from typing_extensions import Annotated

import typer
from typer import Typer
from rich import print

from fam.database.models import UserTable
from fam.database.schemas import CreateUser
from fam.database import services as app_services
from fam.database.users import services as user_services
from fam.database.db import get_db
from fam.add_command import MAIN
from fam.utils import fAborted, fprint, print_dev_mode
from fam.callback import display_version
from fam.cli import app_cli
from fam import core, filename, utils, action


app = Typer(no_args_is_help=True)

app = utils.add_command(app, MAIN)


@app.command(help="Initializes the application for the account user.")
def init():
    action.init_app_dir()


@app.command(help="Resets the application to zero")
def reset(
    force: Annotated[bool, typer.Option("--force", "-f", help="")] = False,
):

    try:

        app_dir: Path = Path(app_cli.directory.app_dir)

        if force:

            if app_dir.exists():
                action.reset_app(app_dir)
            else:
                fprint("Cannot delete application folder because it cannot be found.")
        else:

            msg: str = (
                "Are you sure you want to reset the app? this action is irreversible. Furthermore, all users with an account will have their data deleted?"
            )

            if typer.confirm(msg):
                action.reset_app(app_dir)
            else:
                raise typer.Abort()

    except typer.Abort as e:
        color: str = "red"
        print(f"[{color}]Aborted[/{color}]")

    except Exception as e:
        print(e)


@app.command(help="")
def delete(
    fam_app: Annotated[
        bool, typer.Option("--app", "-a", help="Delete the app.")
    ] = False,
):

    app_dir: Path = Path(app_cli.directory.app_dir)

    if fam_app:
        if typer.confirm("Are you sure you want to delete the app?"):

            action.delete_app(app_dir)
        else:
            raise typer.Abort()


@app.command(help="User logout.")
def logout():
    try:

        session_file: Path = Path(app_cli.directory.app_dir) / "users" / "session.yaml"

        if session_file.exists():
            session_file.unlink()
            fprint("User logout")

    except FileNotFoundError:
        fprint("User logout")
        raise typer.Abort()

    except Exception as e:
        fprint(e)


@app.command(help="Authenticate a user by providing their username and password.")
def login(
    email: Annotated[
        str,
        typer.Option(
            prompt=True,
            help="Email or username.",
        ),
    ],
    password: Annotated[
        str,
        typer.Option(
            prompt=True,
            hide_input=True,
            help="Password to log in.",
        ),
    ],
):
    # Check if the user is in the database
    with get_db() as db:

        user: UserTable = app_services.get_user_by_email(db, email)

        if user is None:
            fprint("The password or username is invalid.")
            raise typer.Abort()

        if not utils.verify_password(password, user.password):
            fprint("The password or username is invalid.")
            raise typer.Abort()

    # Create a Session in store info in app dir
    action.create_session(user)

    fprint("Connection successful.")


@app.command(help="Register a new user by providing necessary details.")
def signup(
    email: Annotated[str, typer.Option(prompt=True, help="Email or username.")],
    password: Annotated[
        str,
        typer.Option(
            prompt=True,
            confirmation_prompt=True,
            hide_input=True,
            help="Password to sign in.",
        ),
    ],
):

    try:

        with get_db() as db:

            # check if user already exist.
            user: UserTable = app_services.get_user_by_email(db, email)

            if user is not None:

                fprint("The user already exists.")
                raise typer.Abort()

            new_user: CreateUser = action.init_user_account(email, password)

            user_services.create_user(db, new_user)

        fprint("Your account has been successfully created.")

    except typer.Abort as e:
        fAborted()

    except Exception as e:
        print(e)


@app.command(help="Update the application.")
def upgrade():
    """
    Upgrade the project by pulling the latest changes from the Git repository.
    """

    update_file: Path = Path(app_cli.directory.app_dir) / filename.UPDATE

    try:
        # Fetch the latest changes from the remote repository
        subprocess.run(["git", "fetch"], check=True)

        result = subprocess.run(
            ["git", "status", "-uno"], check=True, capture_output=True, text=True
        )

        if "Your branch is behind" in result.stdout:
            subprocess.run(
                ["git", "pull", "origin", "main"], check=True, capture_output=True
            )

            fprint("Project successfully upgraded.")

            # Remove the update check file to allow future checks
            if update_file.exists():
                update_file.unlink()

        else:
            fprint("Your project is up-to-date.")

    except subprocess.CalledProcessError as e:
        typer.echo(f"Error during upgrade: {e}", err=True)


@app.command(
    help="Allows you to synchronize the database with a Cloud service installed on the desktop.",
    no_args_is_help=True,
)
def sync(
    foldername: Annotated[
        str,
        typer.Option(
            "--foldername",
            "-f",
            help="Folder path cloud service install on the computer.",
            prompt="",
        ),
    ] = "",
):
    # Get user session

    # Ask the user for the path to the sync folder

    # Check if the folder exists

    # Check if the path is already synced in the config file

    # Add sync path in the config file

    # Add database to the sync folder

    # Check if the database is not corrupt

    # Print message

    fprint("Database synchronization was completed successfully.")


@app.callback(invoke_without_command=True)
def main(
    ctx: typer.Context,
    version: Annotated[bool, typer.Option("--version", "-v", help="")] = False,
):

    if version:
        display_version()
        return

    if action.check_env() == "dev":
        app_cli.app_name = "Test FAM"
        print_dev_mode()

    app_cli.startup()

    if ctx.invoked_subcommand != "init":

        init_file: Path = Path(app_cli.directory.app_dir) / filename.INIT

        if not init_file.exists():
            fprint(
                "Please use command [green]"
                "init"
                "[/green] to initialize the application."
            )
            raise typer.Abort()

        core.check_for_update()


if __name__ == "__main__":
    app()
