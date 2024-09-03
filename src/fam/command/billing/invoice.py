from typing import Sequence
import typer
from typing_extensions import Annotated
from typer import Typer

from fam import auth
from fam.command.utils import (
    build_choice,
    date_to_timestamp,
    is_valid_date,
    show_choice,
)
from fam.database.db import DatabaseType, get_db
from fam.database.users.models import ClassificationTable, TransactionTable
from fam.enums import BankEnum, FinancialProductEnum
from fam.utils import fAborted, fprint, message_coming_soon, normalize_list
from fam.command.billing import action
from fam.database.users import services as user_services

app = Typer(help="Allows you to manage invoices.")

invoice_command: dict = {"app": app, "name": "invoice"}


@app.command(help="Allows you to define the amounts needed to pay invoices.")
def payment():
    message_coming_soon()


@app.command()
def build(
    from_: Annotated[
        str, typer.Option("--from", "-f", help="", prompt="Please indicate start date")
    ] = None,
    to_: Annotated[
        str, typer.Option("--to", "-t", help="", prompt="Please indicate the end date")
    ] = None,
    product: Annotated[
        FinancialProductEnum,
        typer.Option(
            "--product",
            "-p",
            prompt="Please indicate for which financial product",
            case_sensitive=True,
        ),
    ] = None,
    bank: Annotated[
        BankEnum,
        typer.Option("--bank", "-b", help="", prompt="Please indicate the bank"),
    ] = None,
):

    try:
        # get user database_url
        database_url: str = auth.get_user_database_url()

        # verify if the date is valide
        date_list: list[str] = [from_, to_]

        for date in date_list:

            if is_valid_date(date) == False:
                fprint("One of the dates does not have the correct format.")
                raise typer.Abort()

        with get_db(db_path=database_url, db_type=DatabaseType.USER) as db:

            db_classification: Sequence[ClassificationTable] = (
                user_services.get_all_classification(db)
            )

            class_dict, class_choice = build_choice(db_classification)

            show_choice(class_choice)

            id_str: str = typer.prompt(
                type=str, text="Please choose classifications separated by commas (,)"
            )

            id_list: list[str] = normalize_list(id_str)

            classification_list: list[str] = []

            for id in id_list:

                key_id: int = int(id)

                classification_table: ClassificationTable | None = class_dict.get(
                    key_id, None
                )

                if classification_table is None:
                    fprint(
                        f"The id '{key_id}' is not valid. The class will be ignored."
                    )
                    continue

                classification_list.append(classification_table.name)

            for name in classification_list:

                # get transaction from date and classification
                db_transaction: Sequence[TransactionTable] = (
                    user_services.get_transaction_by_date_product_bank_classification(
                        db=db,
                        date_from=date_to_timestamp(from_),
                        date_to=date_to_timestamp(to_),
                        classsification_name=name,
                        product=product,
                        bank=bank,
                    )
                )

                if len(db_transaction) == 0:
                    fprint(
                        f"No transaction for classification with identifier {name}.",
                        color="yellow",
                    )

                    continue

                # Build each classification with colonne Subcategory | Amount Subcategory | Paiement Porportion | Amount with Proportion
                action.generate_invoice_table(
                    classification_name=name,
                    invoice_title=f"Invoice for {name} transaction: {bank.value.upper()} - {product.value.capitalize()}",
                    transaction_list=db_transaction,
                )

    except typer.Abort:
        fAborted()

    except Exception as e:
        print(e)
