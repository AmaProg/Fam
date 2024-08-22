from typing import Any
from sqlalchemy import ScalarResult, Transaction
from typer import Typer
from pandas import DataFrame

import pandas as pd

from fam import auth
from fam.database.db import DatabaseType, get_db
from fam.database.users.models import AccountTable, TransactionTable
from fam.utils import fprint
from fam.database.users import services as user_services

app = Typer(help="Allows you to manage the expenditure section of the budget.")

expense_command: dict[str, Any] = {"app": app, "name": "expense"}


@app.command(help="Allows you to define which account is used for expenses.")
def allocation():
    pass


@app.command(
    help="Allows you to construct the section in charge of the income statement."
)
def build():

    # Get user session
    session = auth.get_user_session()

    database_url = session["database_url"]

    with get_db(db_path=database_url, db_type=DatabaseType.USER) as db:

        # Get expense account id from database
        expense_account: AccountTable = user_services.get_account_id_by_name(
            db, "expense"
        )

        # Get all transactions with expense account id
        expense_transaction: ScalarResult[TransactionTable] | None = (
            user_services.get_transaction_by_account_id(
                db, account_id=expense_account.id
            )
        )
        expense_section: dict[str, float] = {}

        for expense in expense_transaction:

            if expense.category.name in expense_section.keys():
                expense_section[expense.category.name] += expense.amount

            else:
                expense_section.update({expense.category.name: expense.amount})

        # build expense section
        # data = [
        #     {
        #         "description": expense.description,
        #         "amount": expense.amount,
        #         "date": expense.date,
        #     }
        #     for expense in expense_transaction
        # ]

        df = pd.Series(data=expense_section)

    # fprint(df.groupby("description").sum().reset_index())
    fprint(f"\n{df}")
