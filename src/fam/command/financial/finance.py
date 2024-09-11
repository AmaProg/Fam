from copy import copy
from datetime import datetime
from typing_extensions import Annotated
from typing import Any
import typer
from typer import Typer
from rich.table import Table
from rich.console import Console

from fam import auth
from fam.command import financial
from fam.database.db import DatabaseType, get_db


app = Typer(
    help="Finance allows you to visualize your entire financial situation.",
    no_args_is_help=True,
)

finance_command: dict[str, Any] = {"app": app, "name": "finance"}


@app.command(help="Allows you to view the income statement.")
def income_statement():

    database_url: str = auth.get_user_database_url()

    income_statement_table: Table = Table(
        title="Income statement",
        title_justify="center",
    )

    income_statement_table.add_column(
        header="detail".capitalize(),
    )

    income_statement_table.add_column(
        header=str(datetime.now().year),
    )

    with get_db(db_path=database_url, db_type=DatabaseType.USER) as db:

        income_statement_table, total_income = financial.income_section.create_table(
            db=db,
            income_table=copy(income_statement_table),
        )
        income_statement_table, total_expense = financial.expense_section.create_table(
            db=db,
            expense_table=copy(income_statement_table),
        )

    income_statement_table.add_row(
        "",
    )

    net_income: float = round(total_income - total_expense, 2)

    income_statement_table.add_row(
        "Net Income",
        str(net_income),
    )

    console: Console = Console()

    console.print(income_statement_table)


@app.callback()
def finance_callback():
    pass
