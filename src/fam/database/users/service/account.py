from copy import copy
from typing import Sequence
import typing_extensions
from sqlalchemy.orm import Session
from sqlalchemy import Select, select
from sqlalchemy.exc import SQLAlchemyError

from fam.database.users.models import AccountTable
from fam.database.users.schemas import AccountSchemas


def create_account_by_account_model(
    db: Session,
    account_schemas_list: list[AccountSchemas],
) -> list[AccountTable]:

    try:

        account_table_list: list[AccountTable] = []

        for account in account_schemas_list:

            new_account: AccountTable = AccountTable(**account.model_dump())

            account_table_list.append(new_account)

        db.add_all(account_table_list)
        db.commit()

        for account_table in account_table_list:

            db.refresh(account_table)

        return account_table_list

    except SQLAlchemyError as e:
        db.rollback()
        raise


def get_account_id_by_name(db: Session, account_name) -> AccountTable | None:

    try:
        query: Select = select(AccountTable).where(AccountTable.name == account_name)

        account: AccountTable = db.scalar(query)

        return account
    except SQLAlchemyError as e:
        db.rollback()
        raise
