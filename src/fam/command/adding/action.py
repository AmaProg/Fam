from copy import copy
from pathlib import Path
from tkinter import filedialog
from typing import Any
from pandas import DataFrame
from pandas import DataFrame
from sqlalchemy.orm import Session
import typer
import pandas as pd

from fam.command.utils import date_to_timestamp_by_bank, show_choice
from fam.database.users.models import (
    T,
    SubCategoryTable,
    TransactionTable,
)
from fam.database.users.schemas import CreateTransactionBM
from fam.enums import BankEnum, FinancialProductEnum
from fam.bank.bmo import bmo
from fam.database.users import services as user_services
from fam.system.file import File
from fam.utils import fprint, get_user_dir_from_database_url
from fam.bank import constants as kbank


def open_dialog_file(bank: str) -> str:
    csv_filename: str = filedialog.askopenfilename(
        title=f"select the statement for the {bank} bank",
        filetypes=(("CSV files", "*.csv"),),
    )

    return csv_filename


def read_csv_by_bank(filename: str, bank: BankEnum) -> DataFrame | None:

    func: dict[BankEnum, Any] = {
        BankEnum.BMO: pd.read_csv(filename, skiprows=1),
        BankEnum.TANGERINE: pd.read_csv(filename),
    }

    df = func.get(bank, None)

    return df


def get_transaction_rule_file(database_url: str) -> Path:
    user_folder: Path = get_user_dir_from_database_url(database_url)
    trans_file: Path = user_folder / "transaction_rule.yaml"

    return trans_file


def add_transaction_to_rule_file(
    database_url: str,
    trans_base_model: CreateTransactionBM,
) -> None:
    try:
        trans_file: Path = get_transaction_rule_file(database_url)

        content: dict[str, Any] = File.read_yaml_file(trans_file.as_posix()) or {}

        data_rule_list: list[dict[str, Any]] = content.get("rule", [])

        data_rule_list.append(trans_base_model.model_dump())

        File.save_yaml_file(trans_file.as_posix(), {"rule": data_rule_list})

    except Exception as e:
        print(f"An error occurred: {e}")


def classify_transaction_manually(
    transaction,
    subcat_choice: list[str],
    class_choice: list[str],
    subcat_dict: dict[int, SubCategoryTable],
    product: FinancialProductEnum,
    bank: BankEnum,
    bank_ins: kbank.BANK_INSTANCE_TYPE,
    db: Session,
    database_url: str,
) -> CreateTransactionBM | None:
    # Classify all transaction

    # show the message to select a subcategory.
    show_choice(subcat_choice)
    subcat_id: int = typer.prompt(
        type=int,
        text=f"Select a category for {transaction[bank_ins.description]}",
    )

    if subcat_id == 0:
        return None

    # show the message to select a classification.
    show_choice(class_choice)
    cls_id: int = typer.prompt(
        type=int,
        text=f"Select a class for {transaction[bank_ins.description]}",
    )

    sub_table: SubCategoryTable = subcat_dict.get(subcat_id, None)

    if sub_table is None:
        raise typer.Abort()

    new_transaction: CreateTransactionBM = CreateTransactionBM(
        description=transaction[bank_ins.description],
        product=product.value,
        amount=transaction[bank_ins.transaction_amount],
        date=date_to_timestamp_by_bank(
            str(transaction[bank_ins.transaction_date]), bank
        ),
        bank_name=bank.value,
        classification_id=cls_id,
        subcategory_id=subcat_id,
        account_id=sub_table.category.account.id,
    )

    trans_table: TransactionTable | None = (
        user_services.get_transaction_by_date_desc_bank(
            db=db,
            date=new_transaction.date,
            desc=new_transaction.description,
            bank=bank,
        )
    )

    if trans_table is not None:
        if typer.confirm(
            text=f"The following description {new_transaction.description} already exists. Do you want to replace it?"
        ):
            user_services.update_transaction_by_desc(
                db, new_transaction.description, new_transaction
            )
            return None
        else:
            return None

    # Ask the user if they want to classify the transaction automatically
    # for next time.
    if typer.confirm(
        "Do you want the next time you see the transaction to be filed automatically?"
    ):
        add_transaction_to_rule_file(
            database_url=database_url,
            trans_base_model=new_transaction,
        )
        fprint("The transaction has been successfully classified.")

    return new_transaction


def get_transaction_from_rules_file(
    database_url: str,
    trans_desc: str,
    product: FinancialProductEnum,
    bank: BankEnum,
) -> CreateTransactionBM | None:

    trans_file: Path = get_transaction_rule_file(database_url)

    content: dict[str, list[dict[str, Any]]] = (
        File.read_yaml_file(trans_file.as_posix()) or {}
    )

    rules: list[dict[str, Any]] = content.get("rule", [])

    for rule in rules:

        if all(
            [
                rule.get("description", None) == trans_desc,
                rule.get("product", None) == product.value,
                rule.get("bank_name", None) == bank.value,
            ]
        ):
            return CreateTransactionBM(**rule)

    return None


def classify_transaction_auto(
    transaction,
    bank_ins: kbank.BANK_INSTANCE_TYPE,
    bank: BankEnum,
    database_url: str,
    product: FinancialProductEnum,
) -> CreateTransactionBM | None:

    old_transaction: CreateTransactionBM | None = get_transaction_from_rules_file(
        product=product,
        bank=bank,
        database_url=database_url,
        trans_desc=transaction[bank_ins.description],
    )

    if old_transaction is None:
        return None

    transaction_classified = CreateTransactionBM(
        description=old_transaction.description,
        product=old_transaction.product,
        amount=transaction[bank_ins.transaction_amount],
        date=date_to_timestamp_by_bank(
            str(transaction[bank_ins.transaction_date]), bank
        ),
        bank_name=old_transaction.bank_name,
        classification_id=old_transaction.classification_id,
        subcategory_id=old_transaction.subcategory_id,
        account_id=old_transaction.account_id,
    )

    return transaction_classified


def is_transaction_auto_classifiable(
    database_url: str,
    trans,
    bank_ins: kbank.BANK_INSTANCE_TYPE,
    bank: BankEnum,
    product: FinancialProductEnum,
) -> bool:

    user_dir: Path = get_user_dir_from_database_url(database_url)

    trans_file: Path = user_dir / "transaction_rule.yaml"

    content = File.read_yaml_file(trans_file.as_posix())

    if content is None:
        return False

    # Prepare comparison values
    trans_desc = trans[bank_ins.description]
    bank_name = bank.value
    financial_product = product.value

    rules_list: list[dict[str, Any]] = content.get("rule", [])

    for idx, rule in enumerate(rules_list):

        if all(
            [
                trans_desc == rule.get("description", None),
                bank_name == rule.get("bank_name", None),
                financial_product == rule.get("product", None),
            ]
        ):
            return True

    return False


def classify_transactions(
    df: DataFrame,
    subcat_choice: list[str],
    class_choice: list[str],
    subcat_dict: dict[int, SubCategoryTable],
    product: FinancialProductEnum,
    bank: BankEnum,
    db: Session,
    database_url: str,
) -> list[TransactionTable]:

    transactions: list[TransactionTable] = []

    bank_ins: kbank.BANK_INSTANCE_TYPE = kbank.BANK_INST[bank]

    for idx, transaction in df.iterrows():
        trans_table: TransactionTable | None = (
            user_services.get_transaction_by_date_desc_bank(
                db=db,
                date=transaction[bank_ins.transaction_date],
                desc=transaction[bank_ins.description],
                bank=bank,
            )
        )

        if trans_table is not None:
            if typer.confirm(
                text=f"The following description {transaction[bank_ins.description]} already exists. Do you want to replace it?"
            ):
                existing_transaction: CreateTransactionBM = CreateTransactionBM(
                    account_id=trans_table.account_id,
                    amount=trans_table.amount,
                    bank_name=trans_table.bank_name,
                    classification_id=trans_table.classification_id,
                    date=trans_table.date,
                    description=trans_table.description,
                    product=trans_table.product,
                    subcategory_id=trans_table.subcategory_id,
                )

                user_services.update_transaction_by_desc(
                    db, transaction[bank_ins.description], existing_transaction
                )
                continue
            else:
                continue

        if is_transaction_auto_classifiable(
            database_url=database_url,
            trans=transaction,
            product=product,
            bank=bank,
            bank_ins=bank_ins,
        ):
            new_transaction: CreateTransactionBM | None = classify_transaction_auto(
                transaction=transaction,
                bank_ins=bank_ins,
                bank=bank,
                database_url=database_url,
                product=product,
            )

            if new_transaction is not None:
                transactions.append(
                    TransactionTable(**copy(new_transaction.model_dump()))
                )
                fprint(
                    f"Transaction {transaction[bank_ins.description]} has been automatically classified."
                )
                continue
            else:
                fprint("The transaction could not be automatically classified.")

        new_transaction: CreateTransactionBM | None = classify_transaction_manually(
            db=db,
            bank=bank,
            bank_ins=bank_ins,
            class_choice=class_choice,
            database_url=database_url,
            transaction=transaction,
            product=product,
            subcat_choice=subcat_choice,
            subcat_dict=subcat_dict,
        )

        if new_transaction is None:
            continue

        # # Classify all transaction
        # transactions: list[TransactionTable] = []

        # bank_ins: kbank.BANK_INSTANCE_TYPE = kbank.BANK_INST[bank]

        # for idx, transaction in df.iterrows():

        #     # show the message to select a subcategory.
        #     show_choice(subcat_choice)
        #     subcat_id: int = typer.prompt(
        #         type=int,
        #         text=f"Select a category for {transaction[bank_ins.description]}",
        #     )

        #     if subcat_id == 0:
        #         continue

        #     # show the message to select a classification.
        #     show_choice(class_choice)
        #     cls_id: int = typer.prompt(
        #         type=int,
        #         text=f"Select a class for {transaction[bank_ins.description]}",
        #     )

        #     sub_table: SubCategoryTable = subcat_dict.get(subcat_id, None)

        #     if sub_table is None:
        #         raise typer.Abort

        #     # Ask the user if they want to classify the transaction automatically
        #     # for next time.

        #     if typer.confirm(
        #         "Do you want the next time you see the transaction to be filed automatically?"
        #     ):
        #         auto_classify_transaction(database_url, transaction[bank_ins.description])
        #         fprint("The transaction has been successfully classified.")

        #     new_transaction: CreateTransactionBM = CreateTransactionBM(
        #         description=transaction[bank_ins.description],
        #         product=product.value,
        #         amount=transaction[bank_ins.transaction_amount],
        #         date=date_to_timestamp_by_bank(
        #             str(transaction[bank_ins.transaction_date]), bank
        #         ),
        #         bank_name=bank.value,
        #         classification_id=cls_id,
        #         subcategory_id=subcat_id,
        #         account_id=sub_table.category.account.id,
        #     )

        #     trans_table: TransactionTable | None = (
        #         user_services.get_transaction_by_date_desc_bank(
        #             db=db,
        #             date=new_transaction.date,
        #             desc=new_transaction.description,
        #             bank=bank,
        #         )
        #     )

        #     if trans_table is not None:
        #         if typer.confirm(
        #             text=f"The following description {new_transaction.description} already exists. Do you want to replace it?"
        #         ):
        #             user_services.update_transaction_by_desc(
        #                 db, new_transaction.description, new_transaction
        #             )
        #             continue
        #         else:
        #             continue

        transactions.append(TransactionTable(**copy(new_transaction.model_dump())))

    return transactions
