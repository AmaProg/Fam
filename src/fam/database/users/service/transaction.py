from copy import copy
from typing import Sequence
from sqlalchemy.orm import Session
from sqlalchemy import Select, select
from sqlalchemy.exc import SQLAlchemyError

from fam.database.users.models import AccountTable, TransactionTable


def get_transaction_by_transaction_type_account(
    db: Session,
    account_name: str,
    transaction_type: str,
) -> Sequence[TransactionTable]:
    try:
        query: Select = (
            select(TransactionTable)
            .join(AccountTable)
            .where(
                AccountTable.name == account_name,
                TransactionTable.transaction_type == transaction_type,
            )
        )

        db_transanction: Sequence[TransactionTable] = db.scalars(query).all()

        return db_transanction

    except:
        db.rollback()
        return []
