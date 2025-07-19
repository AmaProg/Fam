import typer
import subprocess
import shutil


from pathlib import Path
from typing_extensions import Annotated


from typer import Typer
from rich import print


from fam.database.models import UserTable
from fam.database.schemas import CreateUser
from fam.database import services as app_services
from fam.database.users import services as user_services
from fam.database.db import DatabaseType, get_db
from fam.add_command import MAIN
from fam.os import file
from fam.utils import fAborted, fprint, fprint_panel, print_dev_mode
from fam.callback import display_version
from fam.cli import app_cli
from fam import auth, filename, utils, action
from fam.os.settings import settings
from fam.state import Context
from fam.log.log import logger


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
        logger.error(e)


# @app.command(help="")
# def delete(
#     fam_app: Annotated[
#         bool, typer.Option("--app", "-a", help="Delete the app.")
#     ] = False,
# ):

#     app_dir: Path = Path(app_cli.directory.app_dir)

#     if fam_app:
#         if typer.confirm("Are you sure you want to delete the app?"):

#             action.delete_app(app_dir)
#         else:
#             raise typer.Abort()


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
        logger.error(e)


@app.command(help="Authenticate a user by providing their username and password.")
def login(
    email: Annotated[
        str,
        typer.Option(
            "--email",
            "-e",
            prompt=True,
            help="Email or username.",
        ),
    ],
    password: Annotated[
        str,
        typer.Option(
            "--password",
            "-p",
            prompt=True,
            hide_input=True,
            help="Password to log in.",
        ),
    ],
):
    # Check if the user is in the database
    try:
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

    except Exception as e:
        logger.error(e)


@app.command(help="Register a new user by providing necessary details.")
def signup(
    email: Annotated[
        str,
        typer.Option(
            "--email",
            "-e",
            prompt=True,
            help="Email or username.",
        ),
    ],
    password: Annotated[
        str,
        typer.Option(
            "--password",
            "-p",
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
        logger.error(e)


@app.command(help="Update the application.")
def upgrade():
    """
    Upgrade the project by pulling the latest changes from the Git repository.
    """

    database_url: str = Context.database_url

    try:
        result: bool = settings.update.install_new_version()

        if result is True:
            settings.update.apply_database_migrations(
                database_url=database_url,
            )

        else:
            msg: str = (
                "An error occurred while installing the application version. As a result, the database could not be updated as expected. Please re-run the command. If the issue persists, contact the developers."
            )
            fprint_panel(msg=msg, title="Database Migration Fail", color="red")
            raise typer.Abort()

    except Exception as e:
        logger.error(e)


# @app.command(
#     help="Allows you to synchronize the database with a Cloud service installed on the desktop.",
#     no_args_is_help=False,
# )
# def sync(
#     foldername: Annotated[
#         str,
#         typer.Option(
#             "--foldername",
#             "-f",
#             help="Folder path cloud service install on the computer.",
#             prompt="enter the path to the synchronization folder",
#         ),
#     ],
# ):
#     # Get user session
#     with Context.db as db:

#         data: dict[str, str] = {}

#         # Check if the syn folder exists
#         sync_folder: Path = Path(foldername)

#         if not sync_folder.absolute().exists:
#             logger.error("The synchronization folder does not exist.")
#             raise typer.Abort()

#         # Creates a preference file in json format if it does not exist and inject data
#         db_path: Path = Path(db.get_bind().url.database)  # type: ignore
#         preference_filename = db_path.parent.parent / "user_preference.json"

#         file.File.create_file(
#             dir_path=preference_filename.parent,
#             filename=preference_filename.name,
#         )

#         sync_path: Path = sync_folder / db_path.name

#         data["db"] = sync_path.as_posix()

#         file.File.save_file(
#             data=data,
#             path=preference_filename.absolute(),
#             type_file="json",
#         )

#         # Copy the original database to the cloud folder
#         src: str = db_path.as_posix()
#         dst: str = sync_path.as_posix()

#         shutil.copy2(src=src, dst=dst)

#     # Print message
#     fprint("Database synchronization was completed successfully.")


# @app.command(help="Allows you to manage database backups.")
# def backup():
#     pass


@app.command(help="Allows you to retrieve information from your database.")
def db(
    location: Annotated[
        bool,
        typer.Option(
            "--location",
            "-l",
            help="Allows you to retrieve the path to the database location",
        ),
    ] = False,
    goto: Annotated[
        bool,
        typer.Option(
            "--goto-db",
            "-g",
            help="Allows you to open the folder containing the database",
        ),
    ] = False,
):
    # Get user session.
    # database_url: str = auth.get_user_database_url()

    try:

        with Context.db as db:

            db_path: Path = Path(db.get_bind().url.database)  # type: ignore

            if location:
                fprint(db_path.absolute())  # type: ignore

            if goto:
                subprocess.run(["explorer", db_path.absolute().parent])

    except Exception as e:
        logger.error(e)
        fAborted()


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

        settings.update.check_new_version()

    # verification de la connextion du l'utilisateur
    if ctx.invoked_subcommand not in ["logout", "login", "signup", "init", "reset"]:
        Context.database_url = auth.get_user_database_url()
        Context.db = get_db(db_path=Context.database_url, db_type=DatabaseType.USER)  # type: ignore


if __name__ == "__main__":
    app()
