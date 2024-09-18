import pytest
from pandas import DataFrame
from fam.bank.constants import BANK_INSTANCE_TYPE
from fam.bank.bmo import BMO
from fam.enums import BankEnum, FinancialProductEnum
from fam.database.users.schemas import CreateTransactionModel
from fam.bank.statement import BankStatement


@pytest.fixture
def bank_statement():
    return BankStatement()


def test_bmo_credit_card_statement_standardization(
    bank_statement: BankStatement,
    bmo_credit_card_csv_data,
):
    # Simuler les données d'un relevé BMO
    bmo_credit_card_csv_data["Montant de la transaction"] = [100, -50, 36]
    csv_data = DataFrame(data=bmo_credit_card_csv_data)

    # Tester la standardisation pour BMO
    transactions = bank_statement.standardize_statement(
        bank_name=BankEnum.BMO,
        csv_data=csv_data,
        product=FinancialProductEnum.CREDIT_CARD,
    )

    assert len(transactions) == 3
    assert isinstance(transactions[0], CreateTransactionModel)
    assert transactions[0].amount == 100.0
    assert transactions[0].transaction_type == "debit"
    assert transactions[1].amount == 50.0
    assert transactions[1].transaction_type == "credit"


def test_bmo_check_account_statement_standardization(
    bank_statement: BankStatement,
    bmo_check_acount_csv_data,
):
    # Simuler les données d'un relevé BMO
    bmo_check_acount_csv_data[" Montant de la transaction"] = [100, -50, 36]
    csv_data = DataFrame(data=bmo_check_acount_csv_data)

    # Tester la standardisation pour BMO
    transactions = bank_statement.standardize_statement(
        bank_name=BankEnum.BMO,
        csv_data=csv_data,
        product=FinancialProductEnum.CHECKING_ACCOUNT,
    )

    assert len(transactions) == 3
    assert isinstance(transactions[0], CreateTransactionModel)
    assert transactions[0].amount == 100.0
    assert transactions[0].transaction_type == "debit"
    assert transactions[1].amount == 50.0
    assert transactions[1].transaction_type == "credit"


def test_tangerine_credit_card_statement_standardization(
    bank_statement: BankStatement,
    tangerine_credit_card_csv_data,
):
    # Simuler les données d'un relevé BMO
    tangerine_credit_card_csv_data["Montant"] = [17.24, -17.24, 36]
    csv_data = DataFrame(data=tangerine_credit_card_csv_data)

    # Tester la standardisation pour BMO
    transactions = bank_statement.standardize_statement(
        bank_name=BankEnum.TANGERINE,
        csv_data=csv_data,
        product=FinancialProductEnum.CREDIT_CARD,
    )

    assert len(transactions) == 3
    assert isinstance(transactions[0], CreateTransactionModel)
    assert transactions[0].amount == 17.24
    assert transactions[0].transaction_type == "credit"
    assert transactions[1].amount == 17.24
    assert transactions[1].transaction_type == "debit"


def test_tangerine_check_account_statement_standardization(
    bank_statement: BankStatement,
    tangerine_check_account_csv_data,
):
    # Simuler les données d'un relevé BMO
    tangerine_check_account_csv_data["Montant"] = [100, -50, 36]

    csv_data = DataFrame(data=tangerine_check_account_csv_data)

    # Tester la standardisation pour BMO
    transactions = bank_statement.standardize_statement(
        bank_name=BankEnum.TANGERINE,
        csv_data=csv_data,
        product=FinancialProductEnum.CHECKING_ACCOUNT,
    )

    assert len(transactions) == 3
    assert isinstance(transactions[0], CreateTransactionModel)
    assert transactions[0].amount == 100.0
    assert transactions[0].transaction_type == "credit"
    assert transactions[1].amount == 50.0
    assert transactions[1].transaction_type == "debit"


def test_tangerine_check_account_statement_standardization_when_name_desc_merge(
    bank_statement: BankStatement,
    tangerine_check_account_csv_data,
):
    # Simuler les données d'un relevé BMO
    tangerine_check_account_csv_data["Nom"] = [
        "Transfert-1",
        "Transfert-2",
        "Transfert-3",
    ]
    tangerine_check_account_csv_data["Description"] = [
        "Virement-1",
        "Virement-1",
        "Virement-1",
    ]

    csv_data = DataFrame(data=tangerine_check_account_csv_data)

    # Tester la standardisation pour BMO
    transactions = bank_statement.standardize_statement(
        bank_name=BankEnum.TANGERINE,
        csv_data=csv_data,
        product=FinancialProductEnum.CHECKING_ACCOUNT,
    )

    assert len(transactions) == 3
    assert isinstance(transactions[0], CreateTransactionModel)
    assert transactions[0].description == "Transfert-1 Virement-1"


def test_standardize_tangerine_credit_card_statement_without_merge_name_with_description(
    bank_statement: BankStatement,
    tangerine_credit_card_csv_data,
):
    # Simuler les données d'un relevé BMO
    tangerine_credit_card_csv_data["Nom"] = [
        "Transfert-1",
        "Transfert-2",
        "Transfert-3",
    ]
    tangerine_credit_card_csv_data["Description"] = [
        "Virement-1",
        "Virement-1",
        "Virement-1",
    ]

    csv_data = DataFrame(data=tangerine_credit_card_csv_data)

    # Tester la standardisation pour BMO
    transactions = bank_statement.standardize_statement(
        bank_name=BankEnum.TANGERINE,
        csv_data=csv_data,
        product=FinancialProductEnum.CREDIT_CARD,
    )

    assert len(transactions) == 3
    assert isinstance(transactions[0], CreateTransactionModel)
    assert transactions[0].description == "Transfert-1"
