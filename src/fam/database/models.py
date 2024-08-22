from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, declarative_base
import uuid

AppBase = declarative_base()


class UserTable(AppBase):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    email: Mapped[str] = mapped_column(String(64), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(64), nullable=False)
    database_url: Mapped[str] = mapped_column(String(256), nullable=False, unique=True)
