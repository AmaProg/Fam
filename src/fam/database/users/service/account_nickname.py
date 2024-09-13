from copy import copy
from typing import Sequence
from sqlalchemy.orm import Session
from sqlalchemy import Select, select
from sqlalchemy.exc import SQLAlchemyError

from fam.database.users.models import AccountNicknameTable
from fam.database.users.schemas import CreateAccountNicknameModel


def create_nickname_by_bank_account_type_nickname(
    bank_name: str,
    account: str,
    nickname: str,
    db: Session,
) -> None:

    try:

        nickname_model: CreateAccountNicknameModel = CreateAccountNicknameModel(
            bank_name=bank_name,
            account_type=account,
            nickname=nickname,
        )

        new_nickname: AccountNicknameTable = AccountNicknameTable(
            **nickname_model.model_dump()
        )

        db.add(new_nickname)
        db.commit()

    except:
        db.rollback()
        raise


def get_account_nickname(db: Session) -> Sequence[AccountNicknameTable]:

    try:

        query: Select = select(AccountNicknameTable)

        db_account_nickname: Sequence[AccountNicknameTable] = db.scalars(query).all()

        return db_account_nickname

    except:
        db.rollback()
        return []
