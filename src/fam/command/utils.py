from datetime import datetime
from typing import Any, Literal, Sequence
from rich import print
import typer

from fam.database.users.models import T
from fam.enums import BankEnum


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

    columns = [choice[i * max_row : (i + 1) * max_row] for i in range(max_coloum)]

    space: int = longest_word(choice) + 2

    for i in range(len(columns)):
        columns[i].extend([""] * (max_row - len(columns[i])))

    for row in zip(*columns):
        print("\t".join(f"{item:<{space}}" for item in row))


def date_to_timestamp_by_bank(date_str: str, bank: BankEnum) -> int:
    """
    Converts a date string in the YYYYMMDD format to a Unix timestamp.

    :param date_str: Date string in the YYYYMMDD format
    :return: Unix timestamp corresponding to the date, or None if the date is invalid
    """

    func: dict[BankEnum, datetime] = {
        BankEnum.BMO: datetime.strptime(date_str, "%Y%m%d"),
        BankEnum.TANGERINE: datetime.now(),
    }
    # Convert the string to a datetime object
    date_obj = func.get(bank, datetime.now())

    # Convert the datetime object to a Unix timestamp
    timestamp = int(date_obj.timestamp())

    return timestamp


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
