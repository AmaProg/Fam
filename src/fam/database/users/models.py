from sqlalchemy.orm import Mapped, mapped_column, relationship, declarative_base
from sqlalchemy import ForeignKey


UserBase = declarative_base()


class AccountTable(UserBase):
    __tablename__ = "account"

    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)

    # Définir la relation avec CategoryTable
    category: Mapped["CategoryTable"] = relationship(
        "CategoryTable", back_populates="account"
    )

    transaction: Mapped["TransactionTable"] = relationship(
        "TransactionTable", back_populates="account"
    )


class CategoryTable(UserBase):
    __tablename__ = "category"

    id: Mapped[int] = mapped_column(
        nullable=False, autoincrement=True, primary_key=True
    )
    name: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=True)
    account_id: Mapped[int] = mapped_column(
        ForeignKey("account.id", ondelete="CASCADE"),
        nullable=False,
    )
    # ----- Relationship -----
    account: Mapped["AccountTable"] = relationship(
        "AccountTable", back_populates="category"
    )
    transaction: Mapped["TransactionTable"] = relationship(
        "TransactionTable", back_populates="category"
    )
    sub_category: Mapped["SubCategoryTable"] = relationship(
        "SubCategoryTable", back_populates="category"
    )
    # ----- End Relationship -----


class SubCategoryTable(UserBase):
    __tablename__ = "subcategory"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(nullable=False)
    category_id: Mapped[int] = mapped_column(
        ForeignKey("category.id", ondelete="CASCADE"),
        nullable=False,
    )
    category: Mapped["CategoryTable"] = relationship(
        "CategoryTable", back_populates="sub_category"
    )


class ClassificationTable(UserBase):
    __tablename__ = "classification"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(nullable=False)
    transaction: Mapped["TransactionTable"] = relationship(
        "TransactionTable",
        back_populates="classification",
    )


class TransactionTable(UserBase):
    __tablename__ = "transaction"

    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)
    description: Mapped[str] = mapped_column(nullable=True)
    amount: Mapped[float] = mapped_column(nullable=True)
    date: Mapped[int] = mapped_column(nullable=True)

    # ----- ForeignKey -----
    account_id: Mapped[int] = mapped_column(
        ForeignKey("account.id", ondelete="CASCADE"), nullable=False
    )
    subcategory_id: Mapped[int] = mapped_column(
        ForeignKey("category.id", ondelete="CASCADE"), nullable=False
    )
    classification_id: Mapped[int] = mapped_column(
        ForeignKey("classification.id", ondelete="CASCADE"), nullable=False
    )
    # ----- End ForeignKey -----

    # ----- Relationship -----
    account: Mapped["AccountTable"] = relationship(
        "AccountTable",
        back_populates="transaction",
    )
    category: Mapped["CategoryTable"] = relationship(
        "CategoryTable",
        back_populates="transaction",
    )
    classification: Mapped["ClassificationTable"] = relationship(
        "ClassificationTable",
        back_populates="transaction",
    )
    # ----- End relationship -----
