from typing import Sequence
from pandas import DataFrame
from sqlalchemy.orm import Session
import typer

from fam.command.adding import process
from fam.command.utils import build_choice
from fam.database.users import service
from fam.database.users.models import (
    ClassificationTable,
    SubCategoryTable,
    TransactionTable,
)
from fam.enums import BankEnum, FinancialProductEnum
from fam.utils import fprint, is_empty_list


def add_new_statement(
    db: Session,
    database_url: str,
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

    transaction_list: list[TransactionTable] = process.categorize_transaction(
        df=df,
        subcat_choice=subcat_choice,
        class_choice=class_choice,
        subcat_dict=subcat_dict,
        product=product,
        bank=bank,
        db=db,
        database_url=database_url,
        nickname_id=nickname_id,
    )

    # Save all transactions that have been categorized in the database
    service.transaction.create_transaction(db, transaction_list)
