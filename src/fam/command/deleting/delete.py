from typing_extensions import Annotated
from typing import Any
import typer
from typer import Typer

app = Typer(help="The action of removing things.")

delete_command: dict[str, Any] = {"app": app, "name": "delete"}


@app.command(help="Delete backup files.")
def backup():
    pass


@app.callback()
def delete_callback() -> None:
    pass
