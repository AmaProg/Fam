from typing_extensions import Annotated
from typing import Any, Sequence
import typer
from typer import Typer
from rich.console import Console

from fam import auth
from fam.command.utils import build_choice, show_choice
from fam.database.db import DatabaseType, get_db
from fam.database.users.models import SubCategoryTable
from fam.database.users import services as user_service
from fam.utils import fprint

app = Typer(help="Manage subcategories in the database.")

subcategory_command: dict[str, Any] = {"app": app, "name": "subcategory"}


@app.command()
def list():
    # Get user session
    session = auth.get_user_session()

    database_url: str = session["database_url"]

    with get_db(db_path=database_url, db_type=DatabaseType.USER) as db:
        # Get all Subcategory
        subcat_table: Sequence[SubCategoryTable] = user_service.get_all_subcategory(
            db=db
        )

        if len(subcat_table) == 0:
            fprint("No subcategories found")
            raise typer.Abort()

        subcat_dict, subcat_choise = build_choice(subcat_table, "categogy")

        show_choice(subcat_choise)


@app.callback()
def subcatecory_main():
    pass
