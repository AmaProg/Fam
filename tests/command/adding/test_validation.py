from sqlalchemy.orm import Session

from fam.command.adding.validation import is_auto_categorized
from fam.database.users.schemas import CreateTransactionModel
from fam.enums import BankEnum, FinancialProductEnum


def test_is_auto_categorized_when_transaction_table_list_is_empty(
    mock_get_transaction_by_desc_nickname_bank_product,
    bmo_credit_card_standardize_statement_list,
):

    mock_get_transaction_by_desc_nickname_bank_product.return_value = None

    result, transaction = is_auto_categorized(
        db=Session(),
        transaction_model=bmo_credit_card_standardize_statement_list[0],
        transaction_table_list=[],
    )

    mock_get_transaction_by_desc_nickname_bank_product.assert_called_once()

    assert result == False
    assert transaction == None


def test_is_auto_categorized_when_transaction_is_not_auto_categorize(
    db_transaction,
    mock_get_transaction_by_desc_nickname_bank_product,
    bmo_credit_card_standardize_statement_list,
):
    db_transaction.auto_categorize = False

    mock_get_transaction_by_desc_nickname_bank_product.return_value = db_transaction

    result, transaction = is_auto_categorized(
        db=Session(),
        transaction_model=bmo_credit_card_standardize_statement_list[0],
        transaction_table_list=[],
    )

    mock_get_transaction_by_desc_nickname_bank_product.assert_called_once()

    assert result == False


def test_is_auto_categorized_when_transaction_is_auto_categorize(
    db_transaction,
    mock_get_transaction_by_desc_nickname_bank_product,
    bmo_credit_card_standardize_statement_list,
):
    db_transaction.auto_categorize = True

    mock_get_transaction_by_desc_nickname_bank_product.return_value = db_transaction

    result, transaction = is_auto_categorized(
        db=Session(),
        transaction_model=bmo_credit_card_standardize_statement_list[0],
        transaction_table_list=[],
    )

    mock_get_transaction_by_desc_nickname_bank_product.assert_called_once()

    assert result == True


def test_is_auto_categorized_when_transaction_is_auto_categorize_in_memory_list(
    db_transaction,
    mock_get_transaction_by_desc_nickname_bank_product,
    bmo_credit_card_standardize_statement_list,
):
    db_transaction.description = "Marche IGA"
    db_transaction.account_nickname_id = 1
    db_transaction.bank_name = BankEnum.BMO.value
    db_transaction.product = FinancialProductEnum.CREDIT_CARD.value
    db_transaction.auto_categorize = True

    model = bmo_credit_card_standardize_statement_list[0]
    model.description = "Marche IGA"
    model.account_nickname_id = 1
    model.bank_name = BankEnum.BMO.value
    model.product = FinancialProductEnum.CREDIT_CARD.value

    mock_get_transaction_by_desc_nickname_bank_product.return_value = None

    result, transaction = is_auto_categorized(
        db=Session(),
        transaction_model=model,
        transaction_table_list=[db_transaction],
    )

    mock_get_transaction_by_desc_nickname_bank_product.assert_called_once()

    assert result == True


def test_is_auto_categorized_when_transaction_is_not_auto_categorize_in_memory_list(
    db_transaction,
    mock_get_transaction_by_desc_nickname_bank_product,
    bmo_credit_card_standardize_statement_list,
):
    db_transaction.description = "Marche IGA"
    db_transaction.account_nickname_id = 1
    db_transaction.bank_name = BankEnum.BMO.value
    db_transaction.product = FinancialProductEnum.CREDIT_CARD.value
    db_transaction.auto_categorize = False

    model = bmo_credit_card_standardize_statement_list[0]
    model.description = "Marche IGA"
    model.account_nickname_id = 1
    model.bank_name = BankEnum.BMO.value
    model.product = FinancialProductEnum.CREDIT_CARD.value

    mock_get_transaction_by_desc_nickname_bank_product.return_value = None

    result, transaction = is_auto_categorized(
        db=Session(),
        transaction_model=model,
        transaction_table_list=[db_transaction],
    )

    mock_get_transaction_by_desc_nickname_bank_product.assert_called_once()

    assert result == False
