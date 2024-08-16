from sqlalchemy.orm import Mapped, mapped_column, relationship, declarative_base
from sqlalchemy import ForeignKey

UserBase = declarative_base()


class CategoryTable(UserBase):
    __tablename__ = "category"

    id: Mapped[int] = mapped_column(
        nullable=False, autoincrement=True, primary_key=True
    )
    category_name: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)
    account_id: Mapped[int] = mapped_column(
        ForeignKey("account.id", ondelete="CASCADE"),
        nullable=False,
    )
    # Définir la relation avec AccountTable
    account = relationship("AccountTable", back_populates="categories")


class AccountTable(UserBase):
    __tablename__ = "account"

    id: Mapped[int] = mapped_column(
        nullable=False, autoincrement=True, primary_key=True
    )
    account_name: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)

    # Définir la relation avec CategoryTable
    categories = relationship(
        "CategoryTable", cascade="all, delete-orphan", back_populates="account"
    )
