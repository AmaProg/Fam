from typing import Sequence
from sqlalchemy.orm import Session
from sqlalchemy import Select, select

from fam.database.users.models import BankingInstitutionTable
from fam.database.users.schemas import CreateInstitutionModel
from sqlalchemy.exc import SQLAlchemyError
from fam.utils import fprint


def create_new_bank_institution_by_name(db: Session, institution_name: str) -> None:
    try:

        lower_institution_name: str = institution_name.lower()

        new_institution: CreateInstitutionModel = CreateInstitutionModel(
            name=lower_institution_name
        )

        institution_table: BankingInstitutionTable = BankingInstitutionTable(
            **new_institution.model_dump()
        )

        db.add(institution_table)
        db.commit()

    except SQLAlchemyError as e:
        db.rollback()
        raise


def get_all_bank_institution(db: Session) -> Sequence[BankingInstitutionTable]:

    try:
        query: Select = select(BankingInstitutionTable)

        institution_list: Sequence[BankingInstitutionTable] = db.scalars(query).all()

        return institution_list

    except SQLAlchemyError as e:

        db.rollback()
        return []
