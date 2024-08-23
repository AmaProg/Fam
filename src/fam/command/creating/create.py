from copy import copy
from typing import Any, Sequence
from sqlalchemy import ScalarResult
from typing_extensions import Annotated
from typer import Typer

from rich import print
import typer

from fam import auth
from fam.database.db import DatabaseType, get_db
from fam.database.users.models import AccountTable, CategoryTable, SubCategoryTable
from fam.database.users.schemas import CategoryBM, CreateSubCategory
from fam.enums import AccountSection
from fam.utils import fAborted, fprint
from fam.database.users import services as user_services
from fam.command.utils import build_choice

app = Typer(
    help="Creates bank accounts and expense or income categories.",
    no_args_is_help=True,
)

create_command: dict[str, Any] = {"app": app, "name": "create"}


@app.command(
    help="Allows you to create expense or income categories.",
)
def category(
    name: Annotated[
        str,
        typer.Option(
            "--name",
            "-n",
            help="Category name.",
            prompt="What is the name of the category?",
        ),
    ] = None,
    account_type: Annotated[
        AccountSection,
        typer.Option(
            "--account",
            "-a",
            help="Name of the account which groups the categories.",
            case_sensitive=False,
            show_choices=True,
            prompt="What is the category type?",
        ),
    ] = None,
    desc: Annotated[
        str,
        typer.Option(
            "--desc",
            "-d",
            help="Description of the category.",
            prompt="Give a description to the category",
            show_choices=False,
        ),
    ] = "",
):

    try:

        # Get session file
        session = auth.get_user_session()

        database_url: str = session["database_url"]

        with get_db(database_url, DatabaseType.USER) as db:

            # Check if the category is alredy in the database
            cat_table: CategoryTable | None = user_services.get_category_by_name(
                db,
                name,
            )

            if cat_table is not None:
                fprint("The category is already present.")
                raise typer.Abort()

            # add category
            account_table: AccountTable | None = user_services.get_account_id_by_name(
                db, account_type.value
            )

            if account_table is None:
                raise typer.Abort()

            cat_base_model: CategoryBM = CategoryBM(
                name=name,
                description=desc,
                account_id=account_table.id,
            )

            user_services.create_new_category(db, cat_base_model)

        # print success added category
        fprint("The category was added successfully.")

    except typer.Abort as e:
        fAborted()

    except Exception as e:
        print(e)

    pass


@app.command()
def subcategory():
    try:
        # Get user session
        session = auth.get_user_session()

        database_url = session["database_url"]

        with get_db(db_path=database_url, db_type=DatabaseType.USER) as db:

            # Get all category and build choice
            cat: Sequence[CategoryTable] = user_services.get_all_category(db)

            if cat is None or len(cat) == 0:
                fprint("Please create a category before adding a bank statement.")
                raise typer.Abort

            cat_dict, cat_choice = build_choice(cat)

            typer.echo(cat_choice)
            cat_id = typer.prompt(type=int, text="\nSelect de category")

            category_table: CategoryTable | None = cat_dict.get(cat_id, None)

            ans: str = typer.prompt(
                type=str, text="Please enter the subcategories separating them with (,)"
            )

            list_sub_cat: list = ans.split(",")

            subcategories: list[SubCategoryTable] = []

            for idx, sub in enumerate(list_sub_cat):
                new_sub_cat: CreateSubCategory = CreateSubCategory(
                    name=sub,
                    category_id=category_table.id,  # type: ignore
                )

                subcategories.append(SubCategoryTable(**copy(new_sub_cat.model_dump())))

            # Save category in the database
            user_services.create_subcategory(db, subcategories)

        fprint("The subcategories have been added successfully.")

    except FileNotFoundError:
        fprint("Please log in")
        fAborted()

    except typer.Abort:
        fAborted()

    except Exception as e:
        fprint(e)
