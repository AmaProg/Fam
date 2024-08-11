from pathlib import Path
import shutil
from sys import version
import typer
from typing_extensions import Annotated
from typer import Typer

from fam.enums import BankEnum, FinancialProductEnum
from fam.add import MAIN
from fam.utils import fprint
from rich import print
from fam.callback import display_version
from fam.cli import app_cli
from fam import utils, action


app = Typer(no_args_is_help=True)

app = utils.add_command(app, MAIN)


@app.command(help="Initializes the application for the account user.")
def init():
    action.init_app_dir()


@app.command(help="Resets the application to zero")
def reset(
    force: Annotated[bool, typer.Option("--force", "-f", help="")] = False,
):

    try:

        app_dir: Path = Path(app_cli.directory.app_dir)

        if force:

            if app_dir.exists():
                action.reset_app(app_dir)
            else:
                fprint("Cannot delete application folder because it cannot be found.")
        else:

            msg: str = (
                "Are you sure you want to reset the application? this action is irreversible"
            )

            if typer.confirm(msg):
                action.reset_app(app_dir)
            else:
                raise typer.Abort()

    except typer.Abort as e:
        color: str = "red"
        print(f"[{color}]Aborted[/{color}]")

    except Exception as e:
        print(e)


@app.command(help="")
def delete(
    fam_app: Annotated[
        bool, typer.Option("--app", "-a", help="Delete the app.")
    ] = False,
):

    app_dir: Path = Path(app_cli.directory.app_dir)

    if fam_app:
        if typer.confirm("Are you sure you want to delete the app?"):

            action.delete_app(app_dir)
        else:
            raise typer.Abort()


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
        return

    app_cli.startup()


if __name__ == "__main__":
    app()
