from typing import Sequence
from sqlalchemy.orm import Session
from fam.database.users import service
from fam.database.users.models import TransactionTable
from fam.enums import AccountSectionEnum, TransactionTypeEnum


def fetch_transaction(
    db: Session,
    account_section: AccountSectionEnum,
    transaction_type: TransactionTypeEnum,
) -> Sequence[TransactionTable]:

    db_transaction: Sequence[TransactionTable] = (
        service.transaction.get_transaction_by_transaction_type_account(
            db=db,
            account_name=account_section.value,
            transaction_type=transaction_type.value,
        )
    )

    return db_transaction
