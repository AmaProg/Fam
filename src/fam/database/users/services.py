from sqlalchemy.orm import Session
from sqlalchemy import Select, select
from fam.database.schemas import CreateUser
from fam.database.models import User


def create_user(db: Session, user: CreateUser):

    new_user: User = User(**user.model_dump())

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
