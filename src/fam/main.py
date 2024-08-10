import typer
from typing_extensions import Annotated
from typer import Typer

from fam.enums import BankEnum, FinancialProductEnum
from fam.add import MAIN
from fam.utils import fprint
from rich import print
from fam.callback import display_version
from fam import utils
from fam import action


app = Typer(no_args_is_help=True)

app = utils.add_command(app, MAIN)


@app.command(help="Initializes the application for the account user.")
def init():
    action.init_app_dir()


@app.command(help="Add bank statements.")
def add(
    bank: Annotated[
        BankEnum,
        typer.Option(..., "--bank", "-b", case_sensitive=False, help="Bank name."),
    ] = BankEnum.BMO,
    product: Annotated[
        FinancialProductEnum,
        typer.Option(
            ..., "--product", "-p", case_sensitive=False, help="Financial product."
        ),
    ] = FinancialProductEnum.CREDIT_CARD,
    statement: Annotated[
        str,
        typer.Option("--statement", "-s", help="Bank statement of the product.."),
    ] = None,
    month: Annotated[
        str,
        typer.Option(
            "--month", "-m", help="Month of bank statement in which it was produced."
        ),
    ] = None,
    year: Annotated[
        str,
        typer.Option(
            "--year", "-y", help="Year of bank statement in which it was produced."
        ),
    ] = None,
):
    pass


@app.command(help="Allows you to retrieve information on the credit products you have.")
def credit(bank, product, solde, month, year):
    pass


@app.callback(invoke_without_command=True)
def main(
    ctx: typer.Context,
    version: Annotated[bool, typer.Option("--version", "-v", help="")] = False,
):
    if version:
        display_version()


if __name__ == "__main__":
    app()
