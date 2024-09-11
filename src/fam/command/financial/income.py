import pandas as pd
from typing import Sequence
from pandas import DataFrame, Series
from rich.table import Table
from sqlalchemy.orm import Session

from fam.command.financial import fetch
from fam.command.financial.statement import (
    add_subcategory,
    group_transaction,
    add_category,
)
from fam.database.users import service
from fam.database.users.models import TransactionTable
from fam.enums import AccountSectionEnum, TransactionTypeEnum
from fam.command import utils


def create_table(db: Session, income_table: Table) -> tuple[Table, float]:

    db_transaction: Sequence[TransactionTable] = fetch.fetch_transaction(
        db=db,
        account_section=AccountSectionEnum.INCOME,
        transaction_type=TransactionTypeEnum.CREDIT,
    )

    df = utils.convert_db_transaction_to_dataframe(db_transaction)

    grouped_category, grouped_subcategory = group_transaction(df)

    income_table.add_row("Incomes")

    for _, category_row in grouped_category.iterrows():

        category_name: str = category_row["category_name"]
        category_amount: float = category_row["amount"]

        add_category(income_table, category_name, category_amount)

        sub_grouped: DataFrame = grouped_subcategory[
            grouped_subcategory["category_name"] == category_name
        ]

        add_subcategory(income_table, sub_grouped)

        income_table.add_row()

    total_income: float = grouped_category["amount"].sum()

    income_table.add_row("Total Income", str(total_income))
    income_table.add_row()

    return income_table, total_income
