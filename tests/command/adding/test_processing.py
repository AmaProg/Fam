from datetime import datetime
from typing import Any
from unittest.mock import patch
from pandas import DataFrame
from pytest import fixture
from sqlalchemy.orm import Session


from fam.bank.statement import BankStatement
from fam.command.adding.processing import (
    categorize_transaction,
    categorize_transaction_automatically,
)
from fam.database.users.models import TransactionTable
from fam.database.users.schemas import CreateTransactionModel
from fam.enums import BankEnum, FinancialProductEnum


@fixture
def mock_standardize_statement():
    with patch.object(BankStatement, "standardize_statement", autospec=True) as mock:
        yield mock


@fixture
def mock_generate_transaction_hash():
    with patch(
        "fam.command.adding.processing.generate_transaction_hash", autospec=True
    ) as mock:
        yield mock


@fixture
def mock_is_auto_categorized():
    with patch(
        "fam.command.adding.processing.is_auto_categorized", autospec=True
    ) as mock:
        yield mock


@fixture
def mock_categorize_transaction_automatically():
    with patch(
        "fam.command.adding.processing.categorize_transaction_automatically",
        autospec=True,
    ) as mock:
        yield mock


@fixture
def mock_categorize_transaction_manually():
    with patch(
        "fam.command.adding.processing.categorize_transaction_manually",
        autospec=True,
    ) as mock:
        yield mock


def test_categorize_transaction_when_statement_is_empty(
    mock_standardize_statement,
):

    mock_standardize_statement.return_value = []

    transaction_table_list = categorize_transaction(
        bank=BankEnum.BMO,
        df=DataFrame(),
        product=FinancialProductEnum.CREDIT_CARD,
        nickname_id=1,
        db=Session(),
        subcat_choice=[],
        class_choice=[],
        subcat_dict={},
    )

    mock_standardize_statement.assert_called_once()
    assert len(transaction_table_list) == 0


def test_categorize_transaction_when_transaction_is_alredy_in_database(
    mock_standardize_statement,
    bmo_credit_card_standardize_statement_list,
    mock_generate_transaction_hash,
    mock_get_transaction_by_hash,
    db_transaction,
    capfd,
):
    hash_id = "123456789"

    db_transaction.hash = hash_id
    del bmo_credit_card_standardize_statement_list[0]
    del bmo_credit_card_standardize_statement_list[1]

    transaction_model: CreateTransactionModel = (
        bmo_credit_card_standardize_statement_list[0]
    )

    mock_standardize_statement.return_value = bmo_credit_card_standardize_statement_list
    mock_generate_transaction_hash.return_value = hash_id
    mock_get_transaction_by_hash.return_value = db_transaction

    categorize_transaction(
        bank=BankEnum.BMO,
        df=DataFrame(),
        product=FinancialProductEnum.CREDIT_CARD,
        nickname_id=1,
        db=Session(),
        subcat_choice=[],
        class_choice=[],
        subcat_dict={},
    )

    mock_standardize_statement.assert_called_once()
    mock_generate_transaction_hash.assert_called_once()
    mock_get_transaction_by_hash.assert_called_once()

    # Capture la sortie
    captured = capfd.readouterr()

    output_cleaned = captured.out.replace("\n", "")

    exception_msg = f"Fam: The following description {transaction_model.description} already exists."

    # Vérifie si le message attendu est dans la sortie
    assert exception_msg in output_cleaned


def test_categorize_transaction_when_transaction_auto_categorize(
    mock_standardize_statement,
    bmo_credit_card_standardize_statement_list,
    mock_generate_transaction_hash,
    mock_get_transaction_by_hash,
    mock_is_auto_categorized,
    mock_categorize_transaction_automatically,
    capfd,
):

    hash_id: str = "123456789"
    del bmo_credit_card_standardize_statement_list[0]
    del bmo_credit_card_standardize_statement_list[1]

    auto_transaction = bmo_credit_card_standardize_statement_list[0]
    auto_transaction.description = "Marche IGA"
    transaction_categorize = auto_transaction

    mock_standardize_statement.return_value = bmo_credit_card_standardize_statement_list
    mock_generate_transaction_hash.return_value = hash_id
    mock_get_transaction_by_hash.return_value = None
    mock_is_auto_categorized.return_value = True, auto_transaction
    mock_categorize_transaction_automatically.return_value = transaction_categorize

    categorize_transaction(
        bank=BankEnum.BMO,
        df=DataFrame(),
        product=FinancialProductEnum.CREDIT_CARD,
        nickname_id=1,
        db=Session(),
        subcat_choice=[],
        class_choice=[],
        subcat_dict={},
    )

    mock_standardize_statement.assert_called_once()
    mock_generate_transaction_hash.assert_called_once()
    mock_get_transaction_by_hash.assert_called_once()
    mock_is_auto_categorized.assert_called_once()
    mock_categorize_transaction_automatically.assert_called_once()

    # Capture la sortie
    captured = capfd.readouterr()

    output_cleaned = captured.out.replace("\n", "")

    exception_msg = f"Fam: Transaction {transaction_categorize.description} has been automatically classified."

    # Vérifie si le message attendu est dans la sortie
    assert exception_msg in output_cleaned


def test_categorize_transaction_when_transaction_categorize_manually(
    mock_standardize_statement,
    bmo_credit_card_standardize_statement_list,
    mock_generate_transaction_hash,
    mock_get_transaction_by_hash,
    mock_is_auto_categorized,
    mock_categorize_transaction_manually,
    capfd,
):

    hash_id: str = "123456789"
    del bmo_credit_card_standardize_statement_list[0]
    del bmo_credit_card_standardize_statement_list[1]

    mock_standardize_statement.return_value = bmo_credit_card_standardize_statement_list
    mock_generate_transaction_hash.return_value = hash_id
    mock_get_transaction_by_hash.return_value = None
    mock_is_auto_categorized.return_value = False, None
    mock_categorize_transaction_manually.return_value = None

    categorize_transaction(
        bank=BankEnum.BMO,
        df=DataFrame(),
        product=FinancialProductEnum.CREDIT_CARD,
        nickname_id=1,
        db=Session(),
        subcat_choice=[],
        class_choice=[],
        subcat_dict={},
    )

    mock_standardize_statement.assert_called_once()
    mock_generate_transaction_hash.assert_called_once()
    mock_get_transaction_by_hash.assert_called_once()
    mock_is_auto_categorized.assert_called_once()

    # Capture la sortie
    captured = capfd.readouterr()

    output_cleaned = captured.out.replace("\n", "")

    exception_msg = f"Fam: The description cannot be categorize."

    # Vérifie si le message attendu est dans la sortie
    assert exception_msg in output_cleaned


def test_categorize_transaction_automatically_when_return_transaction_categorize_successfully(
    db_transaction,
    bmo_credit_card_standardize_statement_list,
):

    transaction_model = bmo_credit_card_standardize_statement_list[0]

    db_transaction.account_id = 5
    db_transaction.classification_id = 10

    transaction_categorize = categorize_transaction_automatically(
        auto_transaction=db_transaction,
        transaction_model=transaction_model,
    )

    assert transaction_categorize.account_id == 5
    assert transaction_categorize.classification_id == 10


def test_categorize_transaction_automatically_when_return_transaction_categorize_no_identical(
    db_transaction,
    bmo_credit_card_standardize_statement_list,
):

    transaction_model = bmo_credit_card_standardize_statement_list[0]

    db_transaction.account_id = 5
    db_transaction.classification_id = 10

    transaction_categorize = categorize_transaction_automatically(
        auto_transaction=db_transaction,
        transaction_model=transaction_model,
    )

    assert transaction_categorize.account_id == 5
    assert transaction_categorize.classification_id != 5


# from pathlib import Path

# from fam import filename
# from fam.command.adding.process import (
#     add_transaction_to_rule_file,
#     classify_transaction_auto,
#     get_transaction_from_rules_file,
#     get_transaction_rule_file,
#     is_transaction_auto_classifiable,
# )
# from fam.database.users.schemas import CreateTransactionModel
# from fam.enums import BankEnum, FinancialProductEnum
# from fam.bank import constants as kbank


# def test_get_transaction_rule_path(database_url):

#     user_dir: Path = Path(
#         r"C:\Users\user_name\AppData\Local\Financial_Advisor_for_Me\users\b5d49fb06b704b55bc4a9188b972ed78"
#     )

#     trans_rule_file: Path = get_transaction_rule_file(database_url)

#     assert (
#         trans_rule_file.as_posix() == (user_dir / filename.TRANSACTION_RULE).as_posix()
#     )


# def test_add_transaction_to_rule_file_when_file_is_empty(
#     mock_read_yaml_file,
#     mock_save_yaml_file,
#     transaction_base_model_bmo_bank,
#     database_url,
# ):

#     mock_read_yaml_file.return_value = None

#     add_transaction_to_rule_file(
#         database_url=database_url,
#         trans_base_model=transaction_base_model_bmo_bank,
#     )

#     mock_read_yaml_file.assert_called_once()
#     mock_save_yaml_file.assert_called_once()

#     path_arg, data_arg = mock_save_yaml_file.call_args[0]

#     assert any(
#         transaction_base_model_bmo_bank.model_dump() == d for d in data_arg["rule"]
#     )


# def test_add_transaction_to_rule_file_when_file_is_not_empty(
#     mock_read_yaml_file,
#     mock_save_yaml_file,
#     transaction_base_model_bmo_bank,
#     database_url,
#     transaction_yaml_file,
# ):

#     mock_read_yaml_file.return_value = transaction_yaml_file

#     add_transaction_to_rule_file(
#         database_url=database_url,
#         trans_base_model=transaction_base_model_bmo_bank,
#     )

#     mock_read_yaml_file.assert_called_once()

#     path_arg, data_arg = mock_save_yaml_file.call_args[0]

#     assert any(
#         transaction_base_model_bmo_bank.model_dump() == d for d in data_arg["rule"]
#     )


# def test_auto_classifiable_with_bank_credit_card_when_no_data_returns_none(
#     mock_read_yaml_file,
#     database_url,
#     BMO_CSV_dataframe,
# ):

#     mock_read_yaml_file.return_value = None

#     first_row = BMO_CSV_dataframe.iloc[0]
#     institution: kbank.BANK_INSTANCE_TYPE = kbank.BANK_INST[BankEnum.BMO]
#     description_header: str = institution.get_description(
#         FinancialProductEnum.CREDIT_CARD
#     )

#     result: bool = is_transaction_auto_classifiable(
#         database_url=database_url,
#         bank=BankEnum.BMO,
#         product=FinancialProductEnum.CREDIT_CARD,
#         trans_desc=first_row[description_header],
#         nickname_id=1,
#     )

#     mock_read_yaml_file.assert_called_once()

#     assert result == False


# def test_auto_classifiable_BMO_credit_card_when_returns_data_invalid(
#     mock_read_yaml_file,
#     transaction_yaml_file,
#     BMO_CSV_dataframe,
#     database_url,
# ):

#     mock_read_yaml_file.return_value = transaction_yaml_file

#     assert mock_read_yaml_file.assert_called_once

#     first_row = BMO_CSV_dataframe.iloc[0]

#     institution: kbank.BANK_INSTANCE_TYPE = kbank.BANK_INST[BankEnum.BMO]

#     result: bool = is_transaction_auto_classifiable(
#         database_url=database_url,
#         bank=BankEnum.BMO,
#         product=FinancialProductEnum.CREDIT_CARD,
#         trans_desc=first_row[
#             institution.get_description(FinancialProductEnum.CREDIT_CARD)
#         ],
#         nickname_id=1,
#     )

#     assert result == False


# def test_auto_classifiable_BMO_credit_card_when_returns_data_valid(
#     mock_read_yaml_file,
#     transaction_yaml_file,
#     BMO_CSV_dataframe,
#     database_url,
# ):

#     mock_read_yaml_file.return_value = transaction_yaml_file

#     assert mock_read_yaml_file.assert_called_once

#     first_row = BMO_CSV_dataframe.iloc[1]

#     institution: kbank.BANK_INSTANCE_TYPE = kbank.BANK_INST[BankEnum.BMO]

#     result: bool = is_transaction_auto_classifiable(
#         database_url=database_url,
#         bank=BankEnum.BMO,
#         product=FinancialProductEnum.CREDIT_CARD,
#         trans_desc=first_row[
#             institution.get_description(FinancialProductEnum.CREDIT_CARD)
#         ],
#         nickname_id=1,
#     )

#     assert result == True


# def test_get_transaction_from_rule_file_when_return_none(
#     mock_read_yaml_file,
#     database_url,
#     BMO_CSV_dataframe,
# ):

#     mock_read_yaml_file.return_value = None

#     row = BMO_CSV_dataframe.iloc[1]

#     institution: kbank.BANK_INSTANCE_TYPE = kbank.BANK_INST[BankEnum.BMO]

#     trans_classified = get_transaction_from_rules_file(
#         database_url=database_url,
#         bank=BankEnum.BMO,
#         product=FinancialProductEnum.CREDIT_CARD,
#         trans_desc=row[institution.get_description(FinancialProductEnum.CREDIT_CARD)],
#         nickname_id=1,
#     )

#     assert trans_classified == None


# def test_get_transaction_from_rule_file_when_return_data(
#     mock_read_yaml_file,
#     database_url,
#     BMO_CSV_dataframe,
#     transaction_yaml_file,
# ):

#     mock_read_yaml_file.return_value = transaction_yaml_file

#     row = BMO_CSV_dataframe.iloc[1]

#     institution: kbank.BANK_INSTANCE_TYPE = kbank.BANK_INST[BankEnum.BMO]

#     trans_classified = get_transaction_from_rules_file(
#         database_url=database_url,
#         bank=BankEnum.BMO,
#         product=FinancialProductEnum.CREDIT_CARD,
#         trans_desc=row[institution.get_description(FinancialProductEnum.CREDIT_CARD)],
#         nickname_id=1,
#     )

#     assert (
#         trans_classified.description
#         == row[institution.get_description(FinancialProductEnum.CREDIT_CARD)]
#     )


# def test_classify_transaction_auto_when_transaction_is_already_in_transaction_rule_file(
#     database_url,
#     BMO_CSV_dataframe,
#     mock_read_yaml_file,
#     transaction_yaml_file,
# ):

#     mock_read_yaml_file.return_value = transaction_yaml_file

#     row = BMO_CSV_dataframe.iloc[1]

#     bank_ins: kbank.BANK_INSTANCE_TYPE = kbank.BANK_INST[BankEnum.BMO]

#     transaction_classified: CreateTransactionModel | None = classify_transaction_auto(
#         bank=BankEnum.BMO,
#         institution=bank_ins,
#         database_url=database_url,
#         financial_product=FinancialProductEnum.CREDIT_CARD,
#         transaction=row.to_dict(),
#         nickname_id=1,
#         hash_id="",
#     )

#     row_dict = transaction_yaml_file.get("rule", [])

#     mock_read_yaml_file.assert_called_once()

#     assert transaction_classified.description == row_dict[0].get("description")
#     assert transaction_classified.account_id == row_dict[0].get("account_id")
