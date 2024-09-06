from typing import Sequence
from sqlalchemy.orm import Session
from sqlalchemy import Select, select
from sqlalchemy.exc import SQLAlchemyError

from fam.database.users.models import CategoryTable
from fam.database.users.schemas import CategorySchemas


def create_new_category(db: Session, cat: CategorySchemas) -> CategoryTable:

    try:

        new_cat: CategoryTable = CategoryTable(**cat.model_dump())

        db.add(new_cat)
        db.commit()
        db.refresh(new_cat)

        return new_cat

    except SQLAlchemyError as e:
        db.rollback()
        raise
