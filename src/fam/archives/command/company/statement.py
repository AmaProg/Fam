from typing import Any, List
import typer

from command.company import income, expense
import fam.utils as utils

app = typer.Typer()

STATEMENT: List[dict[str, Any]] = [income.income_command, expense.expense_command]

utils.add_command(app, STATEMENT)

statement_command: dict[str, Any] = {"app": app, "name": "statement"}
