from typing import Sequence
from pandas import DataFrame, Series
from rich.table import Table
from sqlalchemy.orm import Session

from fam.command.financial import fetch
from fam.command.financial.statement import (
    add_category,
    add_subcategory,
    group_transaction,
)
from fam.database.users import service
from fam.command import utils
from fam.database.users.models import TransactionTable
from fam.enums import AccountSectionEnum, TransactionTypeEnum


def create_table(db: Session, expense_table: Table) -> tuple[Table, float]:

    db_transaction: Sequence[TransactionTable] = fetch.fetch_transaction(
        db=db,
        account_section=AccountSectionEnum.EXPENSE,
        transaction_type=TransactionTypeEnum.DEBIT,
    )

    df = utils.convert_db_transaction_to_dataframe(db_transaction)

    grouped_category, grouped_subcategory = group_transaction(df)

    expense_table.add_row("Expenses")

    for _, category_row in grouped_category.iterrows():

        category_name: str = category_row["category_name"]
        category_amount: float = category_row["amount"]

        add_category(expense_table, category_name, category_amount)

        sub_grouped: DataFrame = grouped_subcategory[
            grouped_subcategory["category_name"] == category_name
        ]

        add_subcategory(expense_table, sub_grouped)

        expense_table.add_row()

    total_expense: float = grouped_category["amount"].sum()

    expense_table.add_row("Total Expenses", str(total_expense))

    return expense_table, total_expense
