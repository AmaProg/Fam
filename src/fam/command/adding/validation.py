from pathlib import Path
from typing import Any

from sqlalchemy.orm import Session
from fam.database.users import service
from fam.database.users.models import TransactionTable
from fam.database.users.schemas import CreateTransactionModel
from fam.enums import BankEnum, FinancialProductEnum
from fam.os.file import File
from fam.utils import get_user_dir_from_database_url, normalize_string


def is_transaction_auto_classifiable(
    database_url: str,
    trans_desc: str,
    bank: BankEnum,
    product: FinancialProductEnum,
    nickname_id: int,
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

    rules_list: list[dict[str, Any]] = content.get("rule", [])

    trans_base_model: CreateTransactionModel | None = matches_transaction_rule(
        rules=rules_list,
        bank=bank.value,
        product=product.value,
        transaction_desc=trans_desc,
        nickname_id=nickname_id,
    )

    return True if trans_base_model is not None else False


def matches_transaction_rule(
    transaction_desc: str,
    product: str,
    bank: str,
    rules: list[dict[str, Any]],
    nickname_id: int,
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
        rule_nickname_id = rule.get("account_nickname_id", "")

        if (
            normalize_string(rule_desc) == normalized_trans_desc
            and normalize_string(rule_product) == normalized_product
            and normalize_string(rule_bank) == normalized_bank
            and rule_nickname_id == nickname_id
        ):
            return CreateTransactionModel(**rule)

    return None


def is_auto_categorized(
    transaction: CreateTransactionModel,
    db: Session,
) -> tuple[bool, None | TransactionTable]:

    db_transaction: TransactionTable = (
        service.transaction.get_transaction_by_desc_nickname_bank_product(
            db=db,
            bank_name=transaction.bank_name,
            nickname_id=transaction.account_nickname_id,
            product_financial=transaction.product,
        )
    )

    if db_transaction is None:
        return False, None

    return transaction.auto_categorize, db_transaction
