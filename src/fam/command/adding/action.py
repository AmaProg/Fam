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
        content: dict[str, Any] | None = File.read_yaml_file(trans_file.as_posix())

        data: dict[str, Any] = {}

        if content is None:
            data.update({"rule": []})

        data_rule_list: list[dict[str, Any]] = data["rule"]

        data_rule_list.append(trans_base_model.model_dump())

        data["rule"] = data_rule_list

        File.save_yaml_file(trans_file.as_posix(), data)

    except:
        pass


def classify_transaction_manually(
    df: DataFrame,
    subcat_choice: list[str],
    class_choice: list[str],
    subcat_dict: dict[int, SubCategoryTable],
    product: FinancialProductEnum,
    bank: BankEnum,
    bank_ins: kbank.BANK_INSTANCE_TYPE,
    db: Session,
    database_url: str,
) -> CreateTransactionBM:
    # Classify all transaction

    for idx, transaction in df.iterrows():

        # show the message to select a subcategory.
        show_choice(subcat_choice)
        subcat_id: int = typer.prompt(
            type=int,
            text=f"Select a category for {transaction[bank_ins.description]}",
        )

        if subcat_id == 0:
            continue

        # show the message to select a classification.
        show_choice(class_choice)
        cls_id: int = typer.prompt(
            type=int,
            text=f"Select a class for {transaction[bank_ins.description]}",
        )

        sub_table: SubCategoryTable = subcat_dict.get(subcat_id, None)

        if sub_table is None:
            raise typer.Abort

        # Ask the user if they want to classify the transaction automatically
        # for next time.

        if typer.confirm(
            "Do you want the next time you see the transaction to be filed automatically?"
        ):
            add_transaction_to_rule_file(
                database_url, transaction[bank_ins.description]
            )
            fprint("The transaction has been successfully classified.")

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
                continue
            else:
                continue

    return new_transaction


def get_transaction_from_rules_file(
    database_url: str,
    trans_desc: str,
    product: FinancialProductEnum,
    bank: BankEnum,
) -> CreateTransactionBM | None:
    trans_file: Path = get_transaction_rule_file(database_url)
    content: dict[str, list[CreateTransactionBM]] | None = File.read_yaml_file(
        trans_file.as_posix()
    )

    if content is None:
        raise typer.Abort()

    rules: list[CreateTransactionBM] | None = content["rule"]

    for rule in rules:

        if all(
            [
                rule.description == trans_desc,
                rule.product == product.value,
                rule.bank_name == bank.value,
            ]
        ):
            return rule

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

    transaction = CreateTransactionBM(
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

    return transaction


def is_transaction_auto_classifiable(
    database_url: str,
    trans,
    bank_ins: kbank.BANK_INSTANCE_TYPE,
    bank: BankEnum,
    product: FinancialProductEnum,
) -> bool:

    user_dir: Path = get_user_dir_from_database_url(database_url).parent.parent

    trans_file: Path = user_dir / "transaction_rule.yaml"

    content = File.read_yaml_file(trans_file.as_posix())

    if content is None:
        return False

    rules: list[dict[str, CreateTransactionBM]] = content["rule"]

    for idx, rule in enumerate(rules):
        for key in rule.keys():
            data = rule[key]

            if all(
                [
                    trans[bank_ins.description] == data.description,
                    bank.value == data.bank_name,
                    product.value == data.product,
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
            df=df,
            product=product,
            subcat_choice=subcat_choice,
            subcat_dict=subcat_dict,
        )

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
