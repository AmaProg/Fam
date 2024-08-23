from datetime import datetime
from typing import Any, Sequence
from rich import print

from fam.database.users.models import T
from fam.enums import BankEnum


def build_choice(items: Sequence[T]):

    item_dict: dict[int, T] = {}
    item_choice: list[str] = []

    for item in items:
        item_dict[item.id] = item
        item_choice.append(f"{item.id}: {item.name}")

    return item_dict, item_choice


def show_choice(choice: list[str]) -> None:
    print("\n".join(choice))


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
