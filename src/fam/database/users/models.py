from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from sqlalchemy.ext.declarative import declarative_base

UserBase = declarative_base()


class CategoryTable(UserBase):
    __tablename__ = "category"

    id: Mapped[int] = mapped_column(
        nullable=False, autoincrement=True, primary_key=True
    )
    name: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)
    account_id: Mapped[int] = mapped_column(
        ForeignKey("account.id", ondelete="CASCADE"),
        nullable=False,
    )


class AccountTable(UserBase):
    __tablename__ = "account"

    id: Mapped[int] = mapped_column(
        nullable=False, autoincrement=True, primary_key=True
    )
    name: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)
    category: Mapped["CategoryTable"] = relationship(
        "category", cascade="all, delete-orphan", back_populates=""
    )
