from unittest.mock import patch
from sqlalchemy.orm import Session
import pytest
import typer

from fam.command.creating.action import create_new_transaction
from fam.database.users.models import AccountNicknameTable
from fam.database.users.schemas import CreateAccountNicknameModel
from fam.enums import FinancialAccountEnum, InstitutionEnum, TransactionTypeEnum
from tests.fixtures.data_fixture import db_transaction


@pytest.fixture
def mock_prompt_choice():
    with patch("fam.command.creating.action.prompt_choice", autospec=True) as mock:
        yield mock


@pytest.fixture
def mock_build_choice():
    with patch("fam.command.creating.action.build_choice", autospec=True) as mock:
        yield mock


@pytest.fixture
def nickname_model():
    account_nickname_model: CreateAccountNicknameModel = CreateAccountNicknameModel(
        account_type="",
        bank_name="",
        nickname="",
    )

    return account_nickname_model


@pytest.fixture
def db_nickname(nickname_model):

    return AccountNicknameTable(**nickname_model.model_dump())


def test_create_new_transaction_when_db_account_nickname_table_return_none(
    mock_get_account_nickname,
    capfd,
):
    mock_get_account_nickname.return_value = []

    with pytest.raises(typer.Abort):

        create_new_transaction(
            amount=0,
            bank=InstitutionEnum.BMO,
            date_value=0,
            db=Session(),
            desc="",
            pay_proportion=0,
            product=FinancialAccountEnum.CD,
            transaction_type=TransactionTypeEnum.DEBIT,
        )

    mock_get_account_nickname.assert_called_once()

    # Capture la sortie
    captured = capfd.readouterr()

    output_cleaned = captured.out.replace("\n", "")

    exception_msg = f"Fam: Please create an account nickname with the create account-nickname command."

    # Vérifie si le message attendu est dans la sortie
    assert exception_msg in output_cleaned


def test_create_new_transaction_when_transaction_is_already_in_database(
    mock_get_account_nickname,
    mock_build_choice,
    mock_prompt_choice,
    mock_get_transaction_by_hash,
    db_transaction,
    db_nickname,
    capfd,
):

    db_nickname.id = 1

    mock_get_account_nickname.return_value = [db_nickname]
    mock_build_choice.return_value = {1: db_nickname}, []
    mock_prompt_choice.return_value = 1
    mock_get_transaction_by_hash.return_value = db_transaction

    pay_ratio: int = 50

    with pytest.raises(typer.Abort):

        create_new_transaction(
            amount=0,
            bank=InstitutionEnum.BMO,
            date_value=0,
            db=Session(),
            desc="",
            pay_proportion=pay_ratio,
            product=FinancialAccountEnum.CD,
            transaction_type=TransactionTypeEnum.DEBIT,
        )

    mock_get_account_nickname.assert_called_once()
    mock_build_choice.assert_called_once()
    mock_prompt_choice.assert_called_once()

    # Capture la sortie
    captured = capfd.readouterr()

    output_cleaned = captured.out.replace("\n", "")

    exception_msg = f"Fam: The transaction already exists in the database."

    # Vérifie si le message attendu est dans la sortie
    assert exception_msg in output_cleaned
