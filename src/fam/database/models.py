from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.ext.declarative import declarative_base

AppBase = declarative_base()


class User(AppBase):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(nullable=False, unique=True, primary_key=True)
    first_name: Mapped[str] = mapped_column(nullable=False, unique=True)
    last_name: Mapped[str] = mapped_column(nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    database_id: Mapped[str] = mapped_column(nullable=False, unique=True)
