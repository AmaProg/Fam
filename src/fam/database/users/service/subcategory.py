from typing import Sequence
from sqlalchemy.orm import Session
from sqlalchemy import Select, select
from sqlalchemy.exc import SQLAlchemyError

from fam.database.users.models import SubCategoryTable
from fam.database.users.schemas import CreateSubCategory


def create_subcategory(db: Session, subcategories: CreateSubCategory) -> None:
    try:

        new_subctegory: SubCategoryTable = SubCategoryTable(
            **subcategories.model_dump()
        )

        db.add(new_subctegory)
        db.commit()
    except SQLAlchemyError as e:
        db.rollback()
        raise
