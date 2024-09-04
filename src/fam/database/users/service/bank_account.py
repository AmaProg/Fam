from typing import Sequence
from sqlalchemy.orm import Session
from sqlalchemy import Select, select
from sqlalchemy.exc import SQLAlchemyError

from fam.database.users.models import BankAcountTable
from fam.database.users.schemas import CreateBankAccount


def create_new_bank_Account(
    db: Session,
    account_type: str,
    name: str,
    amount: float,
    bank_id: int,
) -> None:

    try:
        new_bank_account: CreateBankAccount = CreateBankAccount(
            account_type=account_type,
            amount=amount,
            banking_institution_id=bank_id,
            name=name,
        )

        bank_account_Table: BankAcountTable = BankAcountTable(
            **new_bank_account.model_dump()
        )

        db.add(bank_account_Table)
        db.commit()

    except SQLAlchemyError as e:
        db.rollback()
        raise
