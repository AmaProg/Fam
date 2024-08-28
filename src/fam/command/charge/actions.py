from typing import Sequence
from sqlalchemy.orm import Session

from fam.database.users import services as user_service
from fam.database.users.models import TransactionTable
from fam.command.utils import date_to_timestamp


def get_expense_by_date_range(
    db: Session,
    date_from: str,
    date_to: str,
    account_id: int,
) -> dict[str, float]:

    date_from_int: int = date_to_timestamp(date_from)
    date_to_int: int = date_to_timestamp(date_to)

    transactions: Sequence[TransactionTable] = (
        user_service.get_transaction_by_account_id_date_from_date_to(
            db=db,
            account_id=account_id,
            date_from=date_from_int,
            date_to=date_to_int,
        )
    )

    expense_dict: dict[str, float] = {}

    for expense in transactions:

        if expense.subcategory.category.name in expense_dict.keys():
            expense_dict[expense.subcategory.category.name] += expense.amount
        else:
            expense_dict.update({expense.subcategory.category.name: expense.amount})

    return expense_dict
