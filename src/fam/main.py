from uuid import UUID, uuid4
from pathlib import Path
from typing import Any, Generator
from typing_extensions import Annotated


import typer
from typer import Typer
from sqlalchemy.orm import Session

from fam.database.models import User
from fam.database.schemas import CreateUser
from fam.enums import BankEnum, FinancialProductEnum
from fam.add import MAIN
from fam.system.file import File
from fam.utils import fAborted, fprint
from rich import print
from fam.callback import display_version
from fam.cli import app_cli
from fam import utils, action
from fam.database import services as app_services
from fam.database.users import services as user_services
from fam.database.db import DatabaseType, get_db


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
                "Are you sure you want to reset the application? this action is irreversible"
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


@app.command(help="Add bank statements.")
def add(
    bank: Annotated[
        BankEnum,
        typer.Option(..., "--bank", "-b", case_sensitive=False, help="Bank name."),
    ] = BankEnum.BMO,
    product: Annotated[
        FinancialProductEnum,
        typer.Option(
            ..., "--product", "-p", case_sensitive=False, help="Financial product."
        ),
    ] = FinancialProductEnum.CREDIT_CARD,
    statement: Annotated[
        str,
        typer.Option("--statement", "-s", help="Bank statement of the product.."),
    ] = None,
    month: Annotated[
        str,
        typer.Option(
            "--month", "-m", help="Month of bank statement in which it was produced."
        ),
    ] = None,
    year: Annotated[
        str,
        typer.Option(
            "--year", "-y", help="Year of bank statement in which it was produced."
        ),
    ] = None,
):
    pass


@app.command(help="Allows you to retrieve information on the credit products you have.")
def credit(bank, product, solde, month, year):
    pass


@app.command(help="Authenticate a user by providing their username and password.")
def login(
    name: Annotated[str, typer.Option(..., "--name", "-n", help="User Name.")],
):
    pass


@app.command(help="Register a new user by providing necessary details.")
def signup(
    firstname: Annotated[str, typer.Option(prompt=True)],
    lastname: Annotated[str, typer.Option(prompt=True)],
    password: Annotated[
        str,
        typer.Option(prompt=True, confirmation_prompt=True, hide_input=True, help=""),
    ],
):

    try:
        # check if user already exist.
        with get_db(DatabaseType.APP) as db:

            user: User = app_services.get_user_by_fname_n_lname(db, firstname, lastname)

            if user is not None:

                fprint("The user already exists.")
                raise typer.Abort()

            # Create a unique ID.
            id: UUID = uuid4()

            # Create the user folder with unique ID.
            user_dir: Path = action.create_new_user_folder(id.hex)

            # Create a new sql database for the user.
            db_id: str = action.create_new_database(user_dir)

            # crypt the password
            hash_pwd: str = utils.hash_password(password)

            # create a new user in the app database
            new_user: CreateUser = CreateUser(
                first_name=firstname,
                last_name=lastname,
                password=password,
                database_id=db_id,
            )
            user_services.create_user(db, new_user)

        # save the user path in the config file
        config_path: str = (Path(app_cli.directory.app_dir) / "config.yaml").as_posix()

        yaml_data: dict[str, Any] = File.read_file(config_path, "yaml")

        users_list: list[dict[str, Any]] | None = yaml_data["users"]

        if users_list is None:
            users_list = []

        users_list.append({"database": db_id, "path": (user_dir).as_posix()})

        yaml_data["users"] = users_list

        File.save_file(config_path, yaml_data, "yaml")

        # Print that the user folder created successfully.
        fprint("Your account has been successfully created.")

    except typer.Abort as e:
        fAborted()

    except Exception as e:
        print(e)


@app.callback(invoke_without_command=True)
def main(
    ctx: typer.Context,
    version: Annotated[bool, typer.Option("--version", "-v", help="")] = False,
):

    if version:
        display_version()
        return

    app_cli.startup()


if __name__ == "__main__":
    app()
