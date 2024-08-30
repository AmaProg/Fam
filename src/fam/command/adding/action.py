from copy import copy
from pathlib import Path
from tkinter import filedialog
from typing import Any
from pandas import DataFrame
from pandas import DataFrame
from sqlalchemy.orm import Session
import typer
import pandas as pd

from fam.command.utils import date_to_timestamp_by_bank, prompt_choice
from fam.database.users.models import (
    T,
    SubCategoryTable,
    TransactionTable,
)
from fam.database.users.schemas import CreateTransactionBM
from fam.enums import BankEnum, FinancialProductEnum
from fam.database.users import services as user_services
from fam.system.file import File
from fam.utils import fprint, get_user_dir_from_database_url, normalize_string
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
    subcat_id: int = prompt_choice(
        subcat_choice, "Select a category", transaction[bank_ins.description]
    )

    if subcat_id == 0:
        return None

    # show the message to select a classification.
    cls_id: int = prompt_choice(
        class_choice, "Select a category", transaction[bank_ins.description]
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

    trans_base_model: CreateTransactionBM | None = matches_transaction_rule(
        bank=bank.value,
        product=product.value,
        transaction_desc=trans_desc,
        rules=rules,
    )

    # for rule in rules:

    #     rule_desc: str = rule.get("description", "")
    #     rule_product: str = rule.get("product", "")
    #     rule_bank: str = rule.get("bank_name", "")

    #     if all(
    #         [
    #             normalize_string(rule_desc) == normalize_string(trans_desc),
    #             normalize_string(rule_product) == normalize_string(product.value),
    #             normalize_string(rule_bank) == normalize_string(bank.value),
    #         ]
    #     ):
    #         return CreateTransactionBM(**rule)

    return trans_base_model


def matches_transaction_rule(
    transaction_desc: str,
    product: str,
    bank: str,
    rules: list[dict[str, Any]],
):
    """
    Checks if the details of the transaction match any of the specified rules.

    Args:
        transaction_desc (str): Description of the transaction.
        product (Product): Product associated with the transaction.
        bank (Bank): Bank associated with the transaction.
        rules (list): List of rules to compare against.

    Returns:
        CreateTransactionBM: The matching rule if a match is found, otherwise None.
    """
    normalized_trans_desc = normalize_string(transaction_desc)
    normalized_product = normalize_string(product)
    normalized_bank = normalize_string(bank)

    for rule in rules:

        rule_desc = rule.get("description", "")
        rule_product = rule.get("product", "")
        rule_bank = rule.get("bank_name", "")

        if (
            normalize_string(rule_desc) == normalized_trans_desc
            and normalize_string(rule_product) == normalized_product
            and normalize_string(rule_bank) == normalized_bank
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
    trans_desc: str,
    bank: BankEnum,
    product: FinancialProductEnum,
) -> bool:
    """The function checks if the transaction was automatically classified.

    Returns:
        bool: Returns true if the transaction is in file if false.
    """

    user_dir: Path = get_user_dir_from_database_url(database_url)

    trans_file: Path = user_dir / "transaction_rule.yaml"

    content = File.read_yaml_file(trans_file.as_posix())

    if content is None:
        return False

    # Prepare comparison values
    # bank_name = bank.value
    # financial_product = product.value

    rules_list: list[dict[str, Any]] = content.get("rule", [])

    trans_base_model: CreateTransactionBM | None = matches_transaction_rule(
        rules=rules_list,
        bank=bank.value,
        product=product.value,
        transaction_desc=trans_desc,
    )

    return True if trans_base_model is not None else False

    # for idx, rule in enumerate(rules_list):

    #     if all(
    #         [
    #             trans_desc == rule.get("description", None),
    #             bank_name == rule.get("bank_name", None),
    #             financial_product == rule.get("product", None),
    #         ]
    #     ):
    #         return True

    # return False


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
                date=date_to_timestamp_by_bank(
                    str(transaction[bank_ins.transaction_date]), bank
                ),
                desc=transaction[bank_ins.description],
                bank=bank,
            )
        )

        if trans_table is not None:
            fprint(
                f"The following description {transaction[bank_ins.description]} already exists."
            )
            continue

        if is_transaction_auto_classifiable(
            database_url=database_url,
            trans_desc=transaction[bank_ins.description],
            product=product,
            bank=bank,
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

        transactions.append(TransactionTable(**copy(new_transaction.model_dump())))

    return transactions
