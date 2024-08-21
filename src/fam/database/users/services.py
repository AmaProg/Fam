from sqlalchemy.orm import Session
from sqlalchemy import ScalarResult, Select, select
from sqlalchemy.exc import SQLAlchemyError
from fam.database.schemas import CreateUser
from fam.database.models import User
from fam.database.users.models import (
    AccountTable,
    CategoryTable,
    ClassificationTable,
    TransactionTable,
)
from fam.database.users.schemas import (
    AccountBM,
    CategoryBM,
    CreateClassify,
    CreateTransactionBM,
)


def create_user(db: Session, user: CreateUser):

    new_user: User = User(**user.model_dump())

    db.add(new_user)
    db.commit()
    db.refresh(new_user)


def create_account(db: Session, accounts: list[AccountBM]) -> None:

    try:

        # Créer une liste d'objets AccountTable en utilisant une compréhension de liste
        new_accounts = [AccountTable(**account.model_dump()) for account in accounts]

        # Ajouter tous les nouveaux comptes à la session
        db.add_all(new_accounts)

        # Committer les modifications
        db.commit()

    except SQLAlchemyError as e:
        db.rollback()


def get_category_by_name(
    db: Session, cat_name: str
) -> ScalarResult[CategoryTable] | None:

    try:
        query: Select = select(CategoryTable).filter_by(
            category_name=cat_name,
        )

        cat: ScalarResult[CategoryTable] = db.scalars(query)

        return cat

    except SQLAlchemyError as e:
        db.rollback()


def get_all_category(db: Session) -> ScalarResult[CategoryTable]:

    query: Select = select(CategoryTable)

    all_cat: ScalarResult[CategoryTable] = db.scalars(query)

    return all_cat


def get_account_id_by_name(db: Session, account_name) -> AccountTable | None:

    try:
        query: Select = select(AccountTable).filter_by(
            name=account_name,
        )

        account: AccountTable = db.scalar(query)

        return account
    except SQLAlchemyError as e:
        db.rollback()


def create_new_category(db: Session, cat: CategoryBM) -> None:

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


def create_trans(db: Session) -> None:
    try:

        new_trans: CreateTransactionBM = CreateTransactionBM(
            account_id=1,
            amount=-5.02,
            category_id=1,
            classification_id=1,
            date=12542558,
            description="pomme",
        )
        db.add(TransactionTable(**new_trans.model_dump()))
        db.commit()

    except SQLAlchemyError as e:
        db.rollback()
        print(f"Commit failed: {e}")


def create_new_classification(db: Session, classify: CreateClassify):

    try:
        new_classify: ClassificationTable = ClassificationTable(**classify.model_dump())

        db.add(new_classify)
        db.commit()
        db.refresh(new_classify)
    except:
        db.rollback()


def get_all_classification(db: Session) -> ScalarResult[ClassificationTable]:

    try:
        query: Select = select(ClassificationTable)

        classify: ScalarResult[ClassificationTable] = db.scalars(query)

        return classify
    except:
        db.rollback()


def get_transaction_by_account_id(
    db: Session,
    account_id: int,
) -> ScalarResult[TransactionTable] | None:

    try:

        query: Select = select(TransactionTable).where(
            TransactionTable.account_id == account_id
        )

        account_table: ScalarResult[TransactionTable] = db.scalars(query)

        return account_table

    except:
        db.rollback()
