from typing import Any
from typer import Typer

app = Typer(help="Allows you to manage bank accounts")

bank_command: dict[str, Any] = {"app": app, "name": "bank"}


@app.command(help="Allows you to manage bank accounts.")
def account(bank, solde, account):
    pass
