from typing_extensions import Annotated
from typing import Any
import typer
from typer import Typer

from fam.utils import fprint

app = Typer(help="Financial calculator")

calculator_command: dict[str, Any] = {"app": app, "name": "calculator"}


@app.command()
def reer(
    tmi: Annotated[
        float,
        typer.Option(
            "--tmi",
            "-t",
            help="Taux marginal d'imposition",
            prompt="What is the tmi (%)",
        ),
    ] = 0,
    contribution: Annotated[
        float,
        typer.Option(
            "--contribution",
            "-c",
            help="Contribution amount",
            prompt="What is the contribution",
        ),
    ] = 0,
):

    num: float = contribution * (tmi / 100)
    den: float = 1 - (tmi / 100)

    value = num / den

    fprint(f"You need to borrow a value of {value} $")
