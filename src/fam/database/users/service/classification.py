from copy import copy
from typing import Sequence
from sqlalchemy.orm import Session
from sqlalchemy import Select, select
from sqlalchemy.exc import SQLAlchemyError

from fam.database.users.models import ClassificationTable
from fam.database.users.schemas import ClassifySchemas


def create_new_classification(db: Session, classifies: list[ClassifySchemas]):

    try:
        new_classify: list[ClassificationTable] = [
            ClassificationTable(**classify.model_dump()) for classify in classifies
        ]

        db.add_all(new_classify)
        db.commit()
    except SQLAlchemyError as e:
        db.rollback()
        raise


def get_all_classification(db: Session) -> Sequence[ClassificationTable]:

    try:
        query: Select = select(ClassificationTable)

        classify: Sequence[ClassificationTable] = db.scalars(query).all()

        return classify
    except:
        db.rollback()
        return []
