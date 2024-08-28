from datetime import datetime
from typing import Any, Sequence

from fam.database.users import services
from fam.database.users.models import TransactionTable


def date_to_int(date_str: str):
    date_obj = datetime.strptime(date_str, "%Y%m%d")

    # Convert the datetime object to a Unix timestamp
    timestamp = int(date_obj.timestamp())

    return timestamp


def test_get_transaction_by_account_id_date_from_date_to(prepare_user_database):

    data = prepare_user_database

    input_dict: dict[str, Any] = {
        "account_id": 2,
        "date_from": date_to_int("20240101"),
        "date_to": date_to_int("20240130"),
    }

    transactions: Sequence[TransactionTable] = (
        services.get_transaction_by_account_id_date_from_date_to(
            db=data["session"],
            account_id=input_dict["account_id"],
            date_from=input_dict["date_from"],
            date_to=input_dict["date_to"],
        )
    )

    assert len(transactions) == 2
