from typing import Any, Sequence
from typing_extensions import Annotated
from sqlalchemy import ScalarResult, Transaction
from typer import Typer
from pandas import DataFrame

import pandas as pd
import typer

from fam import auth
from fam.command.charge import actions
from fam.database.db import DatabaseType, get_db
from fam.database.users.models import AccountTable, TransactionTable
from fam.enums import AccountSection
from fam.utils import fprint
from fam.database.users import services as user_services

app = Typer(help="Allows you to manage the expenditure section of the budget.")

expense_command: dict[str, Any] = {"app": app, "name": "expense"}


@app.command(help="Allows you to define which account is used for expenses.")
def allocation():
    pass


@app.command(
    help="Allows you to construct the section in charge of the income statement.",
)
def build(
    from_: Annotated[
        str, typer.Option("--from", "-f", help="Start of transaction.")
    ] = "",
    to_: Annotated[str, typer.Option("--to", "-t", help="End of transaction.")] = "",
):

    try:
        # Get user session
        session = auth.get_user_session()

        database_url = session["database_url"]

        expense_section: dict[str, float] = {}

        with get_db(db_path=database_url, db_type=DatabaseType.USER) as db:

            # Get expense account id from database
            expense_account: AccountTable | None = user_services.get_account_id_by_name(
                db, AccountSection.EXPENSE.value
            )

            if expense_account is None:
                fprint("No expense account was found.")
                raise typer.Abort()

            if from_ != "" or to_ != "":
                expense_section = actions.get_expense_by_date_range(
                    db,
                    date_from=from_,
                    date_to=to_,
                    account_id=expense_account.id,
                )

                if not expense_section:
                    fprint(
                        f"No transactions found for the following date {from_} to {to_}"
                    )
                    return

            else:

                # Get all transactions with expense account id
                expense_transaction: Sequence[TransactionTable] = (
                    user_services.get_transaction_by_account_id(
                        db, account_id=expense_account.id
                    )
                )

                if len(expense_transaction) == 0:
                    fprint("No expense transactions were found.")
                    raise typer.Abort()

                expense_section: dict[str, float] = {}

                for expense in expense_transaction:

                    if expense.subcategory.category.name in expense_section.keys():
                        expense_section[
                            expense.subcategory.category.name
                        ] += expense.amount

                    else:
                        expense_section.update(
                            {expense.subcategory.category.name: expense.amount}
                        )

        df = pd.Series(data=expense_section)

        fprint(f"\n{df}")
    except Exception as e:
        fprint(e)


@app.callback(invoke_without_command=True)
def expense_main(cts: typer.Context):
    pass
