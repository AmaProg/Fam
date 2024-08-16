from sqlalchemy.orm import Session
from sqlalchemy import Select, select
from sqlalchemy.exc import SQLAlchemyError
from fam.database.schemas import CreateUser
from fam.database.models import User
from fam.database.users.models import AccountTable
from fam.database.users.schemas import AccountBM


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
