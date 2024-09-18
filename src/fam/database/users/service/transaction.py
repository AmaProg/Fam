from typing import Sequence
from sqlalchemy.orm import Session
from sqlalchemy import Select, select, Delete, delete
from sqlalchemy.exc import SQLAlchemyError

from fam.database.users.models import AccountTable, TransactionTable
from fam.database.users.schemas import CreateTransactionModel


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


def get_transaction_by_hash(db: Session, hash: str) -> TransactionTable:
    try:

        query: Select = select(TransactionTable).where(TransactionTable.hash == hash)

        db_transaction: TransactionTable = db.scalar(query)

        return db_transaction

    except:
        db.rollback()
        raise


def create_one_transaction(db: Session, transaction: CreateTransactionModel) -> None:

    try:

        new_transaction: TransactionTable = TransactionTable(**transaction.model_dump())

        db.add(new_transaction)
        db.commit()

    except:
        db.rollback()
        raise


def create_transaction(db: Session, transactions: list[TransactionTable]) -> None:

    try:
        db.add_all(transactions)
        db.commit()

    except SQLAlchemyError as e:
        db.rollback()
        print(f"Commit failed: {e}")


def get_transaction_by_desc_nickname_bank_product(
    db: Session,
    nickname_id: int,
    bank_name: str,
    product_financial: str,
    desc: str,
) -> TransactionTable:

    try:
        query: Select = select(TransactionTable).where(
            TransactionTable.description.ilike(desc),
            TransactionTable.account_nickname_id == nickname_id,
            TransactionTable.bank_name == bank_name,
            TransactionTable.product == product_financial,
        )

        db_transaction: TransactionTable = db.scalar(query)

        return db_transaction
    except:
        db.rollback()
        raise


def delete_all_transaction(db: Session) -> None:

    try:
        query: Delete = delete(TransactionTable)

        db.execute(query)
        db.commit()
    except:
        db.rollback()
        raise
