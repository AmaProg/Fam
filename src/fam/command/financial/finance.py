from copy import copy
from typing_extensions import Annotated
from typing import Any
import typer
from typer import Typer
from rich.table import Table
from rich.console import Console

from fam import auth
from fam.command import financial
from fam.database.db import DatabaseType, get_db
from .utils import get_year_range


app = Typer(
    help="Finance allows you to visualize your entire financial situation.",
    no_args_is_help=True,
)

finance_command: dict[str, Any] = {"app": app, "name": "finance"}


@app.command(help="Allows you to view the income statement.")
def income_statement(
    to: Annotated[str, typer.Option("--to", "-t", help="")] = None,
    from_: Annotated[str, typer.Option("--from_", "-f", help="")] = None,
):

    to_date, from_date = get_year_range(from_, to)

    str_date = (
        f"{to_date.year} - {from_date.year}"
        if to_date.year != from_date.year
        else str(from_date.year)
    )

    to_date, from_date = get_year_range(from_, to)

    database_url: str = auth.get_user_database_url()

    income_statement_table: Table = Table(
        title="Income statement",
        title_justify="center",
    )

    income_statement_table.add_column(
        header="detail".capitalize(),
    )

    # add column for the year
    income_statement_table.add_column(
        header=str(str_date),
    )

    with get_db(db_path=database_url, db_type=DatabaseType.USER) as db:

        income_statement_table, total_income = financial.income_section.create_table(
            db=db,
            income_table=copy(income_statement_table),
            to_=to_date,
            from_=from_date,
        )
        income_statement_table, total_expense = financial.expense_section.create_table(
            db=db,
            expense_table=copy(income_statement_table),
            to_=to_date,
            from_=from_date,
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
