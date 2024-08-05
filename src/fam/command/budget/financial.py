from typing import Any
import typer

app = typer.Typer()

financial_command: dict[str, Any] = {"app": app, "name": "budget"}


@app.command()
def build():
    pass
