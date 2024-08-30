from pathlib import Path
from typing import assert_type
from unittest.mock import patch

from pytest import fixture
from fam import filename
from fam.command.adding.action import (
    add_transaction_to_rule_file,
    classify_transaction_auto,
    get_transaction_from_rules_file,
    get_transaction_rule_file,
    is_transaction_auto_classifiable,
)
from fam.database.users.schemas import CreateTransactionBM
from fam.enums import BankEnum, FinancialProductEnum
from fam.bank import constants as kbank


@fixture
def database_url() -> str:
    return "sqlite:///C:/Users/user_name/AppData/Local/Financial_Advisor_for_Me/users/b5d49fb06b704b55bc4a9188b972ed78/db/user_database.db"


def test_get_transaction_rule_path(database_url):

    user_dir: Path = Path(
        r"C:\Users\user_name\AppData\Local\Financial_Advisor_for_Me\users\b5d49fb06b704b55bc4a9188b972ed78"
    )

    trans_rule_file: Path = get_transaction_rule_file(database_url)

    assert (
        trans_rule_file.as_posix() == (user_dir / filename.TRANSACTION_RULE).as_posix()
    )


def test_add_transaction_to_rule_file_when_file_is_empty(
    mock_read_yaml_file,
    mock_save_yaml_file,
    transaction_base_model_bmo_bank,
    database_url,
):

    mock_read_yaml_file.return_value = None

    add_transaction_to_rule_file(
        database_url=database_url,
        trans_base_model=transaction_base_model_bmo_bank,
    )

    assert mock_read_yaml_file.assert_called_once
    assert mock_save_yaml_file.called

    path_arg, data_arg = mock_save_yaml_file.call_args[0]

    assert any(
        transaction_base_model_bmo_bank.model_dump() == d for d in data_arg["rule"]
    )


def test_add_transaction_to_rule_file_when_file_is_not_empty(
    mock_read_yaml_file,
    mock_save_yaml_file,
    transaction_base_model_bmo_bank,
    database_url,
    transaction_yaml_file,
):

    mock_read_yaml_file.return_value = transaction_yaml_file

    add_transaction_to_rule_file(
        database_url=database_url,
        trans_base_model=transaction_base_model_bmo_bank,
    )

    mock_read_yaml_file.assert_called_once()

    path_arg, data_arg = mock_save_yaml_file.call_args[0]

    assert any(
        transaction_base_model_bmo_bank.model_dump() == d for d in data_arg["rule"]
    )


def test_is_transaction_auto_classifiable_when_no_data_returns_none(
    mock_read_yaml_file,
    database_url,
    sample_dataframe,
):

    mock_read_yaml_file.return_value = None

    assert mock_read_yaml_file.assert_called_once

    first_row = sample_dataframe.iloc[0]
    bank_ins: kbank.BANK_INSTANCE_TYPE = kbank.BANK_INST[BankEnum.BMO]

    result: bool = is_transaction_auto_classifiable(
        database_url=database_url,
        bank=BankEnum.BMO,
        product=FinancialProductEnum.CREDIT_CARD,
        trans_desc=first_row[bank_ins.description],
    )

    assert result == False


def test_is_transaction_auto_classifiable_when_returns_data_invalid(
    mock_read_yaml_file, transaction_yaml_file, sample_dataframe, database_url
):

    mock_read_yaml_file.return_value = transaction_yaml_file

    assert mock_read_yaml_file.assert_called_once

    first_row = sample_dataframe.iloc[0]

    bank_ins: kbank.BANK_INSTANCE_TYPE = kbank.BANK_INST[BankEnum.BMO]

    result: bool = is_transaction_auto_classifiable(
        database_url=database_url,
        bank=BankEnum.BMO,
        product=FinancialProductEnum.CREDIT_CARD,
        trans_desc=first_row[bank_ins.description],
    )

    assert result == False


def test_is_transaction_auto_classifiable_when_returns_data_valid(
    mock_read_yaml_file,
    transaction_yaml_file,
    sample_dataframe,
    database_url,
):

    mock_read_yaml_file.return_value = transaction_yaml_file

    assert mock_read_yaml_file.assert_called_once

    first_row = sample_dataframe.iloc[1]

    bank_ins: kbank.BANK_INSTANCE_TYPE = kbank.BANK_INST[BankEnum.BMO]

    result: bool = is_transaction_auto_classifiable(
        database_url=database_url,
        bank=BankEnum.BMO,
        product=FinancialProductEnum.CREDIT_CARD,
        trans_desc=first_row[bank_ins.description],
    )

    assert result == True


def test_get_transaction_from_rule_file_when_return_none(
    mock_read_yaml_file, database_url, sample_dataframe
):

    mock_read_yaml_file.return_value = None

    row = sample_dataframe.iloc[1]

    trans_classified = get_transaction_from_rules_file(
        database_url=database_url,
        bank=BankEnum.BMO,
        product=FinancialProductEnum.CREDIT_CARD,
        trans_desc=row,
    )

    assert trans_classified == None


def test_get_transaction_from_rule_file_when_return_data(
    mock_read_yaml_file,
    database_url,
    sample_dataframe,
    transaction_yaml_file,
):

    mock_read_yaml_file.return_value = transaction_yaml_file

    row = sample_dataframe.iloc[1]

    bank_ins: kbank.BANK_INSTANCE_TYPE = kbank.BANK_INST[BankEnum.BMO]

    trans_classified = get_transaction_from_rules_file(
        database_url=database_url,
        bank=BankEnum.BMO,
        product=FinancialProductEnum.CREDIT_CARD,
        trans_desc=row[bank_ins.description],
    )

    assert trans_classified.description == row[bank_ins.description]


def test_classify_transaction_auto_when_transaction_is_already_in_transaction_rule_file(
    database_url,
    sample_dataframe,
    mock_read_yaml_file,
    transaction_yaml_file,
):

    mock_read_yaml_file.return_value = transaction_yaml_file

    assert mock_read_yaml_file.assert_called_once

    row = sample_dataframe.iloc[1]

    bank_ins: kbank.BANK_INSTANCE_TYPE = kbank.BANK_INST[BankEnum.BMO]

    transaction_classified: CreateTransactionBM | None = classify_transaction_auto(
        bank=BankEnum.BMO,
        bank_ins=bank_ins,
        database_url=database_url,
        product=FinancialProductEnum.CREDIT_CARD,
        transaction=row,
    )

    row_dict = transaction_yaml_file.get("rule", [])

    assert transaction_classified.description == row_dict[0].get("description")
    assert transaction_classified.account_id == row_dict[0].get("account_id")
