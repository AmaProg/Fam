from typing_extensions import Annotated
from typing import Any
import typer
from typer import Typer

from fam import auth
from fam.command.deleting import action
from fam.database.db import DatabaseType, get_db
from fam.utils import fprint

app = Typer(help="The action of removing things.")

delete_command: dict[str, Any] = {"app": app, "name": "delete"}


@app.command(help="Delete backup files.")
def backup():
    pass


@app.command(no_args_is_help=True)
def transaction(
    is_all: Annotated[
        bool,
        typer.Option(
            "--all",
            "-a",
            help="Delete all transactions in the database",
        ),
    ] = False,
):

    database_url: str = auth.get_user_database_url()

    with get_db(db_path=database_url, db_type=DatabaseType.USER) as db:

        if is_all:

            msg: str = (
                "Do you want to delete all transactions in the database? This action is irreversible"
            )

            if typer.confirm(text=msg, abort=True):
                action.delete_all_transaction(db)
                fprint("All transactions have been successfully deleted")


@app.callback()
def delete_callback() -> None:
    pass
