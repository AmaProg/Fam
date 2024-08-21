from pathlib import Path
from typing import Any
from sqlalchemy import ScalarResult
from typing_extensions import Annotated
from typer import Typer

from rich import print
import typer

from fam.cli import app_cli
from fam.database.db import DatabaseType, get_db
from fam.database.users.models import AccountTable, CategoryTable
from fam.database.users.schemas import CategoryBM
from fam.enums import CategorySection
from fam.system.file import File
from fam.utils import fAborted, fprint
from fam.database.table.category import Category
from fam.database.users import services as user_services

app = Typer(
    help="Creates bank accounts and expense or income categories.",
    no_args_is_help=True,
)

create_command: dict[str, Any] = {"app": app, "name": "create"}


@app.command(help="Allows you to create bank accounts.")
def account(bank, name, description):
    pass


@app.command(
    help="Allows you to create expense or income categories.",
    no_args_is_help=True,
)
def category(
    name: Annotated[str, typer.Option(..., "--name", "-n", help="Category name.")],
    account_type: Annotated[
        CategorySection,
        typer.Option(
            ...,
            "--category",
            "-c",
            help="Name of the category which groups the categories.",
            case_sensitive=False,
        ),
    ],
    desc: Annotated[
        str, typer.Option("--desc", "-d", help="Description of the category.")
    ] = "",
):

    try:

        # Get session file
        app_dir: Path = Path(app_cli.directory.app_dir)

        sess_path: Path = app_dir / "users" / "session.yaml"

        session_data: dict[str, Any] = File.read_file(sess_path.as_posix(), "yaml")

        database_url: str = session_data["session"]["database_url"]

        with get_db(database_url, DatabaseType.USER) as db:

            # Check if the category is alredy in the database
            categories: ScalarResult[CategoryTable] | None = (
                user_services.get_category_by_name(db, name)
            )

            if categories is not None:
                for idx, category in enumerate(categories):

                    if (
                        category.name == name
                        and category.account.name == account_type.value
                    ):
                        fprint("The category is already present.")
                        raise typer.Abort()

            # add category
            account_table: AccountTable | None = user_services.get_account_id_by_name(
                db, account_type.value
            )

            if account_table is None:
                raise typer.Abort()

            cat: CategoryBM = CategoryBM(
                name=name,
                description=desc,
                account_id=account_table.id,
            )

            user_services.create_new_category(db, cat)

        # print success added category
        fprint("The category was added successfully.")

    except typer.Abort as e:
        fAborted()

    except Exception as e:
        print(e)

    pass
