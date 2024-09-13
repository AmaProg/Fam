from datetime import datetime
import hashlib
import json
from typing import Any, Literal, Sequence
from pandas import DataFrame
from rich import print
import typer
import pandas as pd

from fam.bank.constants import BANK_INSTANCE_TYPE
from fam.database.users.models import T, TransactionTable
from fam.database.users.schemas import TransactionBaseModel
from fam.enums import BankEnum, FinancialProductEnum


def build_choice(
    items: Sequence[T],
    name: Literal["classify", "categogy", "standard", "nickname"] = "standard",
):

    item_dict: dict[int, T] = {}
    item_choice: list[str] = []

    for item in items:
        item_dict[item.id] = item

        if name == "categogy":
            color: str = "yellow"
            item_choice.append(
                f"{item.id}: {item.name} [{color}]({item.category.name})[/{color}]".capitalize()
            )

        elif name == "nickname":
            color: str = "yellow"
            item_choice.append(
                f"{item.id}: {item.nickname} [{color}]({item.bank_name})[/{color}] - {item.account_type}".capitalize()
            )

        else:
            item_choice.append(f"{item.id}: {item.name}".capitalize())

    return item_dict, item_choice


def show_choice(choice: list[str], max_coloum: int = 3) -> None:

    max_row: int = (len(choice) + max_coloum - 1) // max_coloum

    columns: list[list[str]] = [
        choice[i * max_row : (i + 1) * max_row] for i in range(max_coloum)
    ]

    space: int = longest_word(choice)

    for i in range(len(columns)):
        columns[i].extend([""] * (max_row - len(columns[i])))

    for row in zip(*columns):
        print("\t".join(f"{item:<{space}}" for item in row))


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
        text=f"{msg} for {transac_desc}".strip(),
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
        (
            bank == BankEnum.TANGERINE
            and financial_product == FinancialProductEnum.CREDIT_CARD
        )
        or (
            bank == BankEnum.BMO
            and (
                financial_product == FinancialProductEnum.CHECKING_ACCOUNT
                or financial_product == FinancialProductEnum.SAVE_ACCOUNT
            )
        )
        or (
            bank == BankEnum.TANGERINE
            and (
                financial_product == FinancialProductEnum.CHECKING_ACCOUNT
                or financial_product == FinancialProductEnum.SAVE_ACCOUNT
            )
        )
    ):
        amount_column: str = institution.get_transaction_amount(financial_product)

        df[amount_column] = -df[amount_column]

        return df

    else:
        return df


def convert_db_transaction_to_dataframe(
    db_transaction: Sequence[TransactionTable],
) -> DataFrame:

    # Conversion des transactions en une liste de dictionnaires
    transaction_model_list: list[dict[str, Any]] = [
        TransactionBaseModel(
            class_name=t.classification.name,
            category_name=t.subcategory.category.name,
            subcategory_name=t.subcategory.name,
            amount=t.amount,
            pay_ratio=int(t.payment_proportion * 100),
        ).model_dump()
        for t in db_transaction
    ]

    # Conversion de la liste en DataFrame pandas
    df: DataFrame = pd.DataFrame(data=transaction_model_list)

    return df


def generate_transaction_hash(
    desc: str,
    product_name: str,
    amount_value: float,
    date_value: int,
    bank_name: str,
    nickname_id: int,
):

    transaction: dict[str, Any] = {
        "description": desc,
        "product": product_name,
        "amount": amount_value,
        "date": date_value,
        "bank_name": bank_name,
        "nickname": nickname_id,
    }

    unique_string = json.dumps(transaction, sort_keys=True)

    return hashlib.md5(unique_string.encode()).hexdigest()
