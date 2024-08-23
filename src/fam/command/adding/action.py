from copy import copy
from os import name
from pathlib import Path
from tkinter import filedialog
from typing import Any
from webbrowser import get
from pandas import DataFrame
from pandas import DataFrame
from sqlalchemy import ScalarResult
import typer
import pandas as pd


from fam.command.adding import utils
from fam.database.users.models import (
    T,
    SubCategoryTable,
    ClassificationTable,
    TransactionTable,
)
from fam.database.users.schemas import CreateTransactionBM
from fam.enums import BankEnum
from fam.utils import fprint


def open_dialog_file(bank: str) -> str:
    csv_filename: str = filedialog.askopenfilename(
        title=f"select the statement for the {bank} bank",
        filetypes=(("CSV files", "*.csv"),),
    )

    return csv_filename


def read_csv_by_bank(filename: str, bank: BankEnum) -> DataFrame | None:

    func: dict[BankEnum, Any] = {
        BankEnum.BMO: pd.read_csv(filename, skiprows=1),
        BankEnum.TANGERINE: pd.read_csv(filename),
    }

    df = func.get(bank, None)

    return df


def clear_transaction(transactions: list[TransactionTable]) -> list[TransactionTable]:
    pass
