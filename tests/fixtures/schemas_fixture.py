from pytest import fixture

from fam.command.utils import date_to_timestamp_by_bank
from fam.database.users.schemas import CreateTransactionModel
from fam.enums import BankEnum, FinancialProductEnum
from fam.security import generate_transaction_hash


@fixture
def transaction_base_model_bmo_bank() -> CreateTransactionModel:

    transaction_hash: str = generate_transaction_hash({})

    trans: CreateTransactionModel = CreateTransactionModel(
        hash=transaction_hash,
        description="Metro Epicerie",
        amount=1000,
        date=date_to_timestamp_by_bank("20240825", BankEnum.BMO),
        bank_name=BankEnum.BMO.value,
        product=FinancialProductEnum.CREDIT_CARD.value,
        classification_id=1,
        subcategory_id=3,
        account_id=2,
        account_nickname_id=1,
    )

    return trans
