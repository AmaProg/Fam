from typing_extensions import Annotated
from typing import Any
import typer
from typer import Typer

app = Typer(help="")

update_command: dict[str, Any] = {"app": app, "name": "update"}
