from typing import Any
from typing_extensions import Annotated
from tkinter import filedialog

import typer
import pandas as pd

from enums.bank import BankEnum
from command.company import action
import fam.utils as utils

app = typer.Typer()

expense_command: dict[str, Any] = {"app": app, "name": "expense"}


@app.callback(invoke_without_command=True)
def category(
    bank: Annotated[
        BankEnum, typer.Option(..., "--bank", "-b", help="", case_sensitive=False)
    ],
    create_category: Annotated[
        bool, typer.Option("--create-category", "-c", help="")
    ] = False,
    show_list: Annotated[bool, typer.Option("--show-list", "-s", help="")] = True,
    add_statement: Annotated[
        bool, typer.Option("--add-statement", "-a", help="")
    ] = False,
):

    if create_category:

        if add_statement:
            file = filedialog.askopenfilename(
                title=f"select the statement for the {bank} bank",
                filetypes=(("CSV files", "*.csv"),),
            )

        if bank == BankEnum.BMO:
            df: pd.DataFrame = pd.read_csv(file, skiprows=1)

        action.create_new_expense_category(bank, df)

        utils.fprint(f"The new spending category list was created for {bank} bank")
