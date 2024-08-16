from sqlalchemy.orm import Session
from sqlalchemy import select, Select

from sqlalchemy.exc import SQLAlchemyError

from fam.database.models import User


def get_user_by_fname_n_lname(db: Session, fname: str, lname: str) -> User | None:
    try:
        query: Select = select(User).filter_by(
            first_name=fname,
            last_name=lname,
        )

        user: User = db.scalar(query)

        return user
    except SQLAlchemyError as e:
        db.rollback()


def get_user_by_fname(db: Session, fname: str) -> User | None:
    try:
        query: Select = select(User).filter_by(
            first_name=fname,
        )

        user: User = db.scalar(query)

        return user
    except SQLAlchemyError as e:
        db.rollback()
