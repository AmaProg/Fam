from time import sleep
from typing import Any

import typer
from rich import print


def add_command(app: typer.Typer, commands: list[dict[str, Any]]):

    for command in commands:
        app.add_typer(
            typer_instance=command.get("app", None),
            name=command.get("name", ""),
        )

    return app


def fprint(message):
    color: str = "cyan"
    print(f"[{color}]Fam[/{color}]: {message}")
    sleep(0.2)


def fAborted() -> None:
    color: str = "red"
    print(f"[{color}]Aborted[/{color}]")
