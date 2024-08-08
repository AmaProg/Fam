from typing import Any
from typer import Typer

app = Typer(help="Allows you to manage the expenditure section of the budget.")

expense_command: dict[str, Any] = {"app": app, "name": "expense"}


@app.command(help="Allows you to define which account is used for expenses.")
def allocation():
    pass


@app.command(
    help="Allows you to construct the section in charge of the income statement."
)
def build():
    pass
