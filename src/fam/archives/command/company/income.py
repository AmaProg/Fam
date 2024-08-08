from typing import Any
import typer

app = typer.Typer()

income_command: dict[str, Any] = {"app": app, "name": "income"}
