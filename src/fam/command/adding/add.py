from pathlib import Path
from typing import Any, Sequence
from typing_extensions import Annotated
from pandas import DataFrame
from typer import Typer
import typer

from fam import auth
from fam.command.adding import action
from fam.command.utils import build_choice
from fam.database.db import DatabaseType, get_db
from fam.database.users.models import (
    SubCategoryTable,
    ClassificationTable,
    TransactionTable,
)
from fam.enums import BankEnum, FinancialProductEnum
from fam.utils import fAborted, fprint
from fam.database.users import services as user_services

app = Typer(help="Allows you to add items to the folder.")

add_command: dict[str, Any] = {"app": app, "name": "add"}


@app.command()
def statement(
    bank: Annotated[
        BankEnum,
        typer.Option(
            "--bank",
            "-b",
            help="Name of the bank that generated the bank statement.",
            prompt="which bank does the bank statement come from?",
            show_choices=True,
            case_sensitive=False,
        ),
    ],
    product: Annotated[
        FinancialProductEnum,
        typer.Option(
            "--product",
            "-p",
            help="",
            prompt="What is the financial product?",
            show_choices=True,
            case_sensitive=False,
        ),
    ],
    filename: Annotated[
        str,
        typer.Option(
            "--filename", "-f", help="Path of the bank statement in csv format."
        ),
    ] = "",
):
    try:
        # Get user session.
        session = auth.get_user_session()

        database_url: str = session["database_url"]

        # Get csv file and convert to dataframe
        csv_filename: str = (
            action.open_dialog_file(bank) if filename == "" else filename
        )

        if csv_filename == "":
            raise typer.Abort()

        if Path(csv_filename).suffix.lower() != ".csv":
            fprint("Invalid file format: not a CSV.")
            raise typer.Abort()

        df_csv: DataFrame | None = action.read_csv_by_bank(csv_filename, bank)

        if df_csv is None:
            fprint(f"The {bank.value} bank csv file has been corrupted.")
            raise typer.Abort()

        with get_db(db_path=database_url, db_type=DatabaseType.USER) as db:

            # Get all subcategory
            subcategories: Sequence[SubCategoryTable] | None = (
                user_services.get_all_subcategory(db)
            )

            if subcategories is None or len(subcategories) == 0:
                fprint("Please create a subcategory before adding a bank statement.")
                raise typer.Abort()

            classifies: Sequence[ClassificationTable] | None = (
                user_services.get_all_classification(db)
            )

            if classifies is None:
                fprint(
                    "An error occurred while retrieving the transaction classification. Please recreate classifications again."
                )
                raise typer.Abort()

            # By category build category and classification choice
            subcat_dict, subcat_choice = build_choice(subcategories, "categogy")
            subcat_choice.append("0: skip")
            class_dict, class_choice = build_choice(classifies)

            transactions: list[TransactionTable] = action.classify_transactions(
                df=df_csv,
                subcat_choice=subcat_choice,
                class_choice=class_choice,
                subcat_dict=subcat_dict,
                product=product,
                bank=bank,
                db=db,
                database_url=database_url,
            )

            # Save all transactions that have been categorized in the database
            user_services.create_transaction(db, transactions)

        # print success transaction
        fprint(
            "Assignment of categories to the transaction was successfully completed."
        )

    except FileNotFoundError:
        fprint("Please log in")
        fAborted()

    except typer.Abort as e:
        fAborted()

    except Exception as e:
        fprint(e)
