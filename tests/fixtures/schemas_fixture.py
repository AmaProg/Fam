from pytest import fixture

from fam.command.utils import date_to_timestamp_by_bank
from fam.database.users.schemas import CreateTransactionBM
from fam.enums import BankEnum, FinancialProductEnum


@fixture
def transaction_base_model_bmo_bank() -> CreateTransactionBM:
    trans: CreateTransactionBM = CreateTransactionBM(
        description="Metro Epicerie",
        amount=1000,
        date=date_to_timestamp_by_bank("20240825", BankEnum.BMO),
        bank_name=BankEnum.BMO.value,
        product=FinancialProductEnum.CREDIT_CARD.value,
        classification_id=1,
        subcategory_id=3,
        account_id=2,
    )

    return trans
