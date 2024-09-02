from typing import Sequence
import typer
from typing_extensions import Annotated
from typer import Typer

from fam import auth
from fam.command.utils import date_to_timestamp
from fam.database.db import DatabaseType, get_db
from fam.database.users.models import TransactionTable
from fam.utils import fprint, message_coming_soon
from fam.command.billing import action
from fam.database.users import services as user_services

app = Typer(help="Allows you to manage invoices.")

invoice_command: dict = {"app": app, "name": "invoice"}


@app.command(help="Allows you to define the amounts needed to pay invoices.")
def payment():
    message_coming_soon()


@app.command()
def build(
    from_: Annotated[str, typer.Option("--from", "-f", help="", prompt="")] = "",
    to_: Annotated[str, typer.Option("--to", "-t", help="", prompt="")] = "",
    classification: Annotated[
        str, typer.Option("--classification", "-c", help="", prompt="")
    ] = "",
):

    try:
        # get user database_url
        database_url: str = auth.get_user_database_url()

        # verify if the date is valide

        # verify if the classification is present in the database

        classification_list: list[str] = classification.split(",")

        with get_db(db_path=database_url, db_type=DatabaseType.USER) as db:

            for classification_name in classification_list:

                # get transaction from date and classification
                db_transaction: Sequence[TransactionTable] = (
                    user_services.get_transaction_by_date_classification(
                        db=db,
                        date_from=date_to_timestamp(from_),
                        date_to=date_to_timestamp(to_),
                        classsification_name=classification_name,
                    )
                )

                # Build each classification with colonne Subcategory | Amount Subcategory | Paiement Porportion | Amount with Proportion
                action.generate_invoice_table(
                    classification_name=classification_name,
                    invoice_title="Invoce",
                    transaction_list=db_transaction,
                )

        fprint("")
    except Exception as e:
        print(e)
