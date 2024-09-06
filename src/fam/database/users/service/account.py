from copy import copy
from typing import Sequence
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

            account_table_list.append(copy(AccountTable(**account.model_dump())))

        db.add_all(account_table_list)
        db.commit()

        for account_table in account_schemas_list:

            db.refresh(account_table)

        return account_table_list

    except SQLAlchemyError as e:
        db.rollback()
        raise
