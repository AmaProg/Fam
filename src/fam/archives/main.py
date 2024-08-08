from typing_extensions import Annotated

import typer

import fam.utils as utils
import fam.add as add

app = typer.Typer()

app = utils.add_command(app, add.MAIN)


@app.command(help="Create an empty Fam workspace")
def init():
    pass


@app.command(help="Create new bank branches.")
def create():
    pass


@app.callback(invoke_without_command=True)
def main(
    ctx: typer.Context,
    version: Annotated[
        bool, typer.Option("--version", "-v", help="Reports the version of this tool.")
    ] = False,
):
    pass


if __name__ == "__main__":
    app()
