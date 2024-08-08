from typing import Any
from typer import Typer

app = Typer(help="Creates bank accounts and expense or income categories.")

create_command: dict[str, Any] = {"app": app, "name": "create"}


@app.command(help="Allows you to create bank accounts.")
def account(bank, name, description):
    pass


@app.command(help="Allows you to create expense or income categories.")
def category(bank, name, description, category):
    pass
