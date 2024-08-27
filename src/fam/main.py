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
from fam import utils, action


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
    try:
        # Exécute la commande git pull
        subprocess.run(["git", "pull", "origin", "main"], check=True)
        typer.echo("Project successfully upgraded.")
    except subprocess.CalledProcessError as e:
        typer.echo(f"Error during upgrade: {e}", err=True)


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


if __name__ == "__main__":
    app()
