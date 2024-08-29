from typing_extensions import Annotated
from typing import Any
import typer
from typer import Typer

from fam.utils import fprint

app = Typer(help="The action of getting things")

get_command: dict[str, Any] = {"app": app, "name": "get"}


@app.command()
def backup():

    # Get user session

    # Check if the backup folder exists

    # List the backup files

    # Ask the user which backup file they want

    # Replace original database with the backup

    # Print message

    fprint(f"The {1} backup was successfully recovered.")


@app.callback()
def get_callback() -> None:
    pass
