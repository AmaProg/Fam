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


def test_standardize_bmo_statement(bank_statement: BankStatement):
    # Simuler les données d'un relevé BMO
    csv_data = DataFrame(
        {
            "Date d'inscription": ["20230901", "20230902"],
            "Description": ["Transaction A", "Transaction B"],
            " Montant de la transaction": [100.0, -50.0],
        }
    )

    # Tester la standardisation pour BMO
    transactions = bank_statement.standardize_statement(
        bank_name=BankEnum.BMO,
        csv_data=csv_data,
        product=FinancialProductEnum.CHECKING_ACCOUNT,
    )

    assert len(transactions) == 2
    assert isinstance(transactions[0], CreateTransactionModel)
    assert transactions[0].amount == 100.0
    assert transactions[1].amount == -50.0


def test_standardize_tangerine_statement(bank_statement: BankStatement):
    # Simuler les données d'un relevé Tangerine
    csv_data = DataFrame(
        {
            "Date": ["09/01/2023", "09/02/2023"],
            "Description": ["Transaction C", "Transaction D"],
            "Nom": ["Store 1", "Store 2"],
            "Montant": [200.0, -75.0],
        }
    )

    # Tester la standardisation pour Tangerine
    transactions = bank_statement.standardize_statement(
        bank_name=BankEnum.TANGERINE,
        csv_data=csv_data,
        product=FinancialProductEnum.CHECKING_ACCOUNT,
    )

    assert len(transactions) == 2
    assert isinstance(transactions[0], CreateTransactionModel)
    assert transactions[0].amount == -200.0  # Négatif car inversé dans la logique
    assert transactions[1].amount == 75.0
