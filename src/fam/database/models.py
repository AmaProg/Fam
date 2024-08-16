from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship, declarative_base
import uuid

AppBase = declarative_base()


class User(AppBase):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    first_name: Mapped[str] = mapped_column(nullable=False)
    last_name: Mapped[str] = mapped_column(nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    database_url: Mapped[str] = mapped_column(nullable=False, unique=True)
