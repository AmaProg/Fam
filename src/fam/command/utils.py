from datetime import datetime
from typing import Literal, Sequence
from pandas import DataFrame
from rich import print
import typer

from fam.bank.constants import BANK_INSTANCE_TYPE
from fam.database.users.models import T
from fam.enums import BankEnum, FinancialProductEnum


def build_choice(
    items: Sequence[T], name: Literal["classify", "categogy", "standard"] = "standard"
):

    item_dict: dict[int, T] = {}
    item_choice: list[str] = []

    for item in items:
        item_dict[item.id] = item

        if name == "categogy":
            item_choice.append(f"{item.id}: {item.name} ({item.category.name})")
        else:
            item_choice.append(f"{item.id}: {item.name}")

    return item_dict, item_choice


def show_choice(choice: list[str], max_coloum: int = 3) -> None:

    max_row: int = (len(choice) + max_coloum - 1) // max_coloum

    columns: list[list[str]] = [
        choice[i * max_row : (i + 1) * max_row] for i in range(max_coloum)
    ]

    space: int = longest_word(choice) + 2

    for i in range(len(columns)):
        columns[i].extend([""] * (max_row - len(columns[i])))

    for row in zip(*columns):
        print("\t".capitalize().join(f"{item:<{space}}".capitalize() for item in row))


def date_to_timestamp_by_bank(date_str: str, bank: BankEnum) -> int:
    """
    Converts a date string to a Unix timestamp based on the bank.

    :param date_str: Date string
    :param bank: Bank enum
    :return: Unix timestamp corresponding to the date, or 0 if the date is invalid
    """
    # Define format strings for each bank
    FORMAT_STRINGS: dict[BankEnum, str] = {
        BankEnum.BMO: "%Y%m%d",
        BankEnum.TANGERINE: "%m/%d/%Y",
    }

    format_str = FORMAT_STRINGS.get(bank)

    if format_str is None:
        raise ValueError(f"Unsupported bank: {bank}")

    try:
        date_obj = datetime.strptime(date_str, format_str)
    except ValueError:
        return 0  # Or handle invalid date string as needed

    return int(date_obj.timestamp())


def date_to_timestamp(date_str: str) -> int:
    """
    Converts a date string in the YYYYMMDD format to a Unix timestamp.

    :param date_str: Date string in the YYYYMMDD format
    :return: Unix timestamp corresponding to the date, or None if the date is invalid
    """
    # Convert the string to a datetime object
    date_obj = datetime.strptime(date_str, "%Y%m%d")

    # Convert the datetime object to a Unix timestamp
    timestamp = int(date_obj.timestamp())

    return timestamp


def prompt_choice(choice: list[str], msg: str, transac_desc: str) -> int:

    show_choice(choice)

    prompt_int: int = typer.prompt(
        type=int,
        text=f"{msg} for {transac_desc}",
    )

    return prompt_int


def longest_word(words) -> int:
    if not words:
        return 0  # Retourne None si la liste est vide

    # Utiliser max avec une fonction clé pour trouver le mot le plus long
    return len(max(words, key=len))


def is_valid_date(date_str: str) -> bool:
    try:

        datetime.strptime(date_str, "%Y%m%d")

        return True

    except ValueError:
        return False


def inverse_amount_sign_by_bank(
    df: DataFrame,
    bank: BankEnum,
    institution: BANK_INSTANCE_TYPE,
    financial_product: FinancialProductEnum,
) -> DataFrame:

    if (
        bank == BankEnum.TANGERINE
        and financial_product == FinancialProductEnum.CREDIT_CARD
    ):
        amount_column: str = institution.get_transaction_amount(financial_product)

        df[amount_column] = -df[amount_column]

        return df

    else:
        return df
