from typing import Sequence
from sqlalchemy.orm import Session

from fam.database.users import service
from fam.database.users.models import ClassificationTable, SubCategoryTable


def get_subcategory_and_classification(
    db: Session,
) -> tuple[Sequence[SubCategoryTable], Sequence[ClassificationTable]]:
    # Get all subcategories
    db_subcategories: Sequence[SubCategoryTable] = (
        service.subcategory.get_subcategories(db)
    )

    # Get all classifications
    db_classification: Sequence[ClassificationTable] = (
        service.classification.get_all_classification(db)
    )

    return db_subcategories, db_classification
