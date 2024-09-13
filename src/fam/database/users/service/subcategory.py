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


def get_subcategories(db: Session) -> Sequence[SubCategoryTable]:

    try:
        query: Select = select(SubCategoryTable)

        all_subcat: Sequence[SubCategoryTable] = db.scalars(query).all()

        return all_subcat
    except:
        db.rollback()
        return []
