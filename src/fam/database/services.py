from sqlalchemy.orm import Session
from sqlalchemy import select, Select

from sqlalchemy.exc import SQLAlchemyError

from fam.database.models import UserTable


def get_user_by_email(db: Session, user_email: str) -> UserTable | None:
    try:
        query: Select = select(UserTable).where(UserTable.email == user_email)

        user: UserTable = db.scalar(query)

        return user

    except SQLAlchemyError as e:
        db.rollback()


def get_user_by_email(db: Session, email: str) -> UserTable | None:
    try:
        query: Select = select(UserTable).where(UserTable.email == email)

        user: UserTable = db.scalar(query)

        return user
    except SQLAlchemyError as e:
        db.rollback()
