from sqlalchemy.orm import Session
from fam.database.users import service
from fam.database.users.models import TransactionTable
from fam.database.users.schemas import CreateTransactionModel
from fam.utils import normalize_string


def is_auto_categorized(
    transaction_model: CreateTransactionModel,
    transaction_table_list: list[TransactionTable],
    db: Session,
) -> tuple[bool, None | TransactionTable]:

    db_transaction: TransactionTable = (
        service.transaction.get_transaction_by_desc_nickname_bank_product(
            db=db,
            bank_name=transaction_model.bank_name,
            nickname_id=transaction_model.account_nickname_id,
            product_financial=transaction_model.product,
            desc=transaction_model.description,
        )
    )

    if db_transaction is not None:
        return db_transaction.auto_categorize, db_transaction

    for table in transaction_table_list:

        if all(
            [
                table.bank_name == transaction_model.bank_name,
                table.account_nickname_id == transaction_model.account_nickname_id,
                table.product == transaction_model.product,
                normalize_string(table.description)
                == normalize_string(transaction_model.description),
            ]
        ):
            return table.auto_categorize, table

    return False, None
