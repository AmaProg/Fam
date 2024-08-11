from typing import Any
from typing_extensions import Annotated
import typer

app = typer.Typer()

bank_command: dict[str, Any] = {"app": app, "name": "bank"}


@app.command("new-branch", help="")
def new_branch(
    bmo: Annotated[
        bool, typer.Option("--bmo", "-b", help="Create a branch for bank BMO.")
    ] = False,
    tangerine: Annotated[
        bool,
        typer.Option("--tangerine", "-t", help="Create a branch for bank Tangerine"),
    ] = False,
):
    pass
