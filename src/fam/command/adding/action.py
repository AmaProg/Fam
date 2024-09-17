from pandas import DataFrame
from sqlalchemy.orm import Session
import typer

from fam.command.adding import processing
from fam.command.utils import build_choice
from fam.database.users import service
from fam.database.users.models import (
    TransactionTable,
)
from fam.enums import BankEnum, FinancialProductEnum
from fam.utils import fprint


def add_new_statement(
    db: Session,
    df: DataFrame,
    product: FinancialProductEnum,
    bank: BankEnum,
    nickname_id: int,
) -> None:

    # Get all subcategories
    db_subcategories, db_classification = (
        service.utils.get_subcategory_and_classification(db)
    )

    if not db_subcategories:
        fprint("Please create a subcategory before adding a bank statement.")
        raise typer.Abort()

    if not db_classification:
        fprint(
            "An error occurred while retrieving the transaction classification. Please recreate classifications again."
        )
        raise typer.Abort()

    # By category build category and classification choice
    subcat_dict, subcat_choice = build_choice(db_subcategories, "categogy")
    subcat_choice.append("0: skip")
    _, class_choice = build_choice(db_classification)

    transaction_list: list[TransactionTable] = processing.categorize_transaction(
        df=df,
        subcat_choice=subcat_choice,
        class_choice=class_choice,
        subcat_dict=subcat_dict,
        product=product,
        bank=bank,
        db=db,
        nickname_id=nickname_id,
    )

    if len(transaction_list) == 0:
        fprint("No transaction has been put into the database")
        raise typer.Abort()

    # Save all transactions that have been categorized in the database
    service.transaction.create_transaction(db, transaction_list)
