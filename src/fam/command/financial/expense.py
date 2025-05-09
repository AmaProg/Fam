from datetime import datetime
from typing import Sequence
from pandas import DataFrame
from rich.table import Table
from sqlalchemy.orm import Session

from fam.command.financial.statement import (
    add_category,
    add_subcategory,
    group_transaction,
)
from fam.database.users import service
from fam.command import utils
from fam.database.users.models import TransactionTable
from fam.enums import AccountSectionEnum, TransactionTypeEnum
from fam.database.users import service


def create_table(
    db: Session,
    expense_table: Table,
    to_: datetime,
    from_: datetime,
) -> tuple[Table, float]:

    db_transaction: Sequence[TransactionTable] = (
        service.transaction.by_transaction_type_and_account(
            db=db,
            account_name=AccountSectionEnum.EXPENSE.value,
            transaction_type=TransactionTypeEnum.DEBIT.value,
            to_=to_,
            from_=from_,
        )
    )

    if len(db_transaction) == 0:
        return expense_table, 0

    df = utils.convert_db_transaction_to_dataframe(db_transaction)

    df = df[df["category_name"] != "Epargne"]
    df = df[df["category_name"] != "Opérations Internes"]

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
