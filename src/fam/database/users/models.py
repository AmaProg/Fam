from itertools import product
from os import name
from typing import TypeVar
from sqlalchemy.orm import Mapped, mapped_column, relationship, declarative_base
from sqlalchemy import CheckConstraint, ForeignKey, CheckConstraint


UserBase = declarative_base()

T = TypeVar("T", bound="BaseTable")


class BaseTable:
    id: int
    name: str
    category: "CategoryTable"


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
        "TransactionTable",
        back_populates="account",
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
    subcategory: Mapped["SubCategoryTable"] = relationship(
        "SubCategoryTable", back_populates="category"
    )
    # ----- End Relationship -----


class SubCategoryTable(UserBase):
    __tablename__ = "subcategory"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=True)
    category_id: Mapped[int] = mapped_column(
        ForeignKey("category.id", ondelete="CASCADE"),
        nullable=False,
    )
    category: Mapped["CategoryTable"] = relationship(
        "CategoryTable", back_populates="subcategory"
    )
    transaction: Mapped["TransactionTable"] = relationship(
        "TransactionTable",
        back_populates="subcategory",
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
    product: Mapped[str] = mapped_column(nullable=False)
    amount: Mapped[float] = mapped_column(nullable=True)
    date: Mapped[int] = mapped_column(nullable=True)
    bank_name: Mapped[str] = mapped_column(nullable=False)
    payment_proportion: Mapped[float] = mapped_column(nullable=False)
    transaction_type: Mapped[str] = mapped_column(nullable=True, default="debit")

    # ----- ForeignKey -----
    subcategory_id: Mapped[int] = mapped_column(
        ForeignKey("subcategory.id", ondelete="CASCADE"),
        nullable=False,
    )
    classification_id: Mapped[int] = mapped_column(
        ForeignKey("classification.id", ondelete="CASCADE"),
        nullable=False,
    )
    account_id: Mapped[int] = mapped_column(
        ForeignKey("account.id", ondelete="CASCADE"),
        nullable=False,
    )
    # ----- End ForeignKey -----

    # ----- Relationship -----
    subcategory: Mapped["SubCategoryTable"] = relationship(
        "SubCategoryTable",
        back_populates="transaction",
    )
    classification: Mapped["ClassificationTable"] = relationship(
        "ClassificationTable",
        back_populates="transaction",
    )
    account: Mapped["AccountTable"] = relationship(
        "AccountTable",
        back_populates="transaction",
    )
    # ----- End relationship -----


class BankingInstitutionTable(UserBase):
    __tablename__ = "banking_institution"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(nullable=False, unique=True)

    bank_account: Mapped["BankAcountTable"] = relationship(
        "BankAcountTable", back_populates="banking_institution"
    )


class BankAcountTable(UserBase):
    __tablename__ = "bank_account"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    account_type: Mapped[str] = mapped_column(nullable=False)
    name: Mapped[str] = mapped_column(nullable=False, unique=True)
    amount: Mapped[float] = mapped_column(nullable=False)
    banking_institution_id: Mapped[int] = mapped_column(
        ForeignKey("banking_institution.id", ondelete="CASCADE"),
        nullable=False,
    )
    banking_institution: Mapped["BankingInstitutionTable"] = relationship(
        "BankingInstitutionTable", back_populates="bank_account"
    )
