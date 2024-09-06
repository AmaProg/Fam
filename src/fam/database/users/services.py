from typing import Sequence
import typing_extensions
import warnings
from sqlalchemy.orm import Session
from sqlalchemy import Select, Update, select, update, text
from sqlalchemy.exc import SQLAlchemyError
from fam.database.schemas import CreateUser
from fam.database.models import UserTable
from fam.database.users.models import (
    AccountTable,
    SubCategoryTable,
    ClassificationTable,
    CategoryTable,
    TransactionTable,
)
from fam.database.users.schemas import (
    AccountSchemas,
    CategorySchemas,
    ClassifySchemas,
    CreateTransactionBM,
)
from fam.enums import (
    AccountSectionEnum,
    BankEnum,
    FinancialProductEnum,
    TransactionTypeEnum,
)


def create_user(db: Session, user: CreateUser):
    try:

        new_user: UserTable = UserTable(**user.model_dump())

        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    except SQLAlchemyError as e:
        print(e)
        db.rollback()


@typing_extensions.deprecated("pomme", category=None)
def create_account(db: Session, accounts: list[AccountSchemas]) -> None:

    try:

        new_accounts = [AccountTable(**account.model_dump()) for account in accounts]

        db.add_all(new_accounts)

        db.commit()

    except SQLAlchemyError as e:
        db.rollback()


def get_category_by_name(db: Session, cat_name: str) -> CategoryTable | None:

    try:
        query: Select = select(CategoryTable).where(CategoryTable.name == cat_name)

        cat: CategoryTable = db.scalar(query)

        return cat

    except SQLAlchemyError as e:
        db.rollback()


def get_all_category(db: Session) -> Sequence[CategoryTable]:

    query: Select = select(CategoryTable)

    all_cat: Sequence[CategoryTable] = db.scalars(query).all()

    return all_cat


def get_all_subcategory(db: Session) -> Sequence[SubCategoryTable]:

    try:
        query: Select = select(SubCategoryTable)

        all_subcat: Sequence[SubCategoryTable] = db.scalars(query).all()

        return all_subcat
    except:
        db.rollback()
        return []


def get_account_id_by_name(db: Session, account_name) -> AccountTable | None:

    try:
        query: Select = select(AccountTable).where(AccountTable.name == account_name)

        account: AccountTable = db.scalar(query)

        return account
    except SQLAlchemyError as e:
        db.rollback()


def create_new_category(db: Session, cat: CategorySchemas) -> None:

    try:

        new_cat: CategoryTable = CategoryTable(**cat.model_dump())

        db.add(new_cat)
        db.commit()
        db.refresh(new_cat)
    except SQLAlchemyError as e:
        db.rollback()


def create_transaction(db: Session, transactions: list[TransactionTable]) -> None:

    try:
        db.add_all(transactions)
        db.commit()

    except SQLAlchemyError as e:
        db.rollback()
        print(f"Commit failed: {e}")


@typing_extensions.deprecated("pomme", category=None)
def create_new_classification(db: Session, classifies: list[ClassifySchemas]):

    try:
        new_classify: list[ClassificationTable] = [
            ClassificationTable(**classify.model_dump()) for classify in classifies
        ]

        db.add_all(new_classify)
        db.commit()
        db.refresh(new_classify)
    except:
        db.rollback()


def get_all_classification(db: Session) -> Sequence[ClassificationTable]:

    try:
        query: Select = select(ClassificationTable)

        classify: Sequence[ClassificationTable] = db.scalars(query).all()

        return classify
    except:
        db.rollback()
        return []


def get_transaction_by_account_id(
    db: Session,
    account_id: int,
) -> Sequence[TransactionTable]:

    try:

        query: Select = select(TransactionTable).where(
            TransactionTable.account_id == account_id
        )

        transaction_table: Sequence[TransactionTable] = db.scalars(query).all()

        return transaction_table

    except:
        db.rollback()
        return []


def get_transaction_by_date_desc_bank(
    db: Session, date: int, desc: str, bank: BankEnum
) -> TransactionTable | None:

    query: Select = select(TransactionTable).where(
        TransactionTable.date == date,
        TransactionTable.description.ilike(desc.upper()),
        TransactionTable.bank_name == bank.value,
    )

    transaction: TransactionTable = db.scalar(query)

    return transaction


def update_transaction_by_desc(db: Session, desc, update_trans: CreateTransactionBM):

    query: Update = (
        update(TransactionTable)
        .where(TransactionTable.description == desc)
        .values(update_trans.model_dump())
    )

    db.execute(query)
    db.commit()


def create_subcategory(db: Session, sub_categories: list[SubCategoryTable]) -> None:
    try:
        db.add_all(sub_categories)
        db.commit()
    except SQLAlchemyError as e:
        print(e)
        db.rollback()


def get_transaction_by_account_id_date_from_date_to(
    db: Session,
    account_id: int,
    date_from: int,
    date_to: int,
) -> Sequence[TransactionTable]:

    try:
        query: Select = select(TransactionTable).where(
            TransactionTable.account_id == account_id,
            TransactionTable.date.between(date_from, date_to),
        )

        trans_table_list: Sequence[TransactionTable] = db.scalars(query).all()

        return trans_table_list

    except Exception as e:
        print(e)
        db.rollback()
        return []


def get_classification_by_name(db: Session, name: str) -> ClassificationTable | None:

    try:
        query: Select = select(ClassificationTable).where(
            ClassificationTable.name == name
        )

        result: ClassificationTable = db.scalar(query)

        return result
    except:
        db.rollback()
        return None


def get_current_alembic_revision(db: Session):
    # Exécuter une requête SQL pour obtenir la version actuelle d'Alembic
    result = db.execute(text("SELECT version_num FROM alembic_version"))
    current_revision = result.scalar()
    return current_revision


def get_transaction_by_date_product_bank_classification(
    db: Session,
    date_from: int,
    date_to: int,
    product: FinancialProductEnum,
    bank: BankEnum,
    classsification_name: str,
) -> Sequence[TransactionTable]:

    try:
        query: Select = (
            select(TransactionTable)
            .join(ClassificationTable)
            .join(AccountTable)
            .where(
                AccountTable.name == AccountSectionEnum.EXPENSE.value,
                ClassificationTable.name == classsification_name,
                TransactionTable.date.between(date_from, date_to),
                TransactionTable.transaction_type == TransactionTypeEnum.DEBIT.value,
                TransactionTable.product == product.value,
                TransactionTable.transaction_type == TransactionTypeEnum.DEBIT.value,
                TransactionTable.bank_name == bank.value,
            )
        )

        result: Sequence[TransactionTable] = db.scalars(query).all()

        return result
    except SQLAlchemyError as e:
        db.rollback()
        print(e)
        return []
