from typing_extensions import Annotated
from typing import Any
import typer
from typer import Typer

from fam import auth
from fam.command.getting import action
from fam.database.db import DatabaseType, get_db
from fam.utils import fprint

app = Typer(help="The action of getting things")

get_command: dict[str, Any] = {"app": app, "name": "get"}


@app.command()
def backup():

    # Get user session

    # Check if the backup folder exists

    # List the backup files

    # Ask the user which backup file they want

    # Replace original database with the backup

    # Print message

    fprint(f"The {1} backup was successfully recovered.")


@app.command(no_args_is_help=True)
def subcategory(
    get_list: Annotated[bool, typer.Option("--list", "-l", help="")] = False,
):

    database_url: str = auth.get_user_database_url()

    with get_db(db_path=database_url, db_type=DatabaseType.USER) as db:

        if get_list:
            action.get_subcategory_from_database(db)


@app.command()
def account_nickname(
    get_list: Annotated[bool, typer.Option("--list", "-l", help="")] = False,
):
    database_url: str = auth.get_user_database_url()

    with get_db(db_path=database_url, db_type=DatabaseType.USER) as db:

        if get_list:
            action.get_account_nickname_from_database(db)


@app.callback()
def get_callback() -> None:
    pass
