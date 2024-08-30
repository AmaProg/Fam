from typing import Any
from unittest import result, runner
from unittest.mock import AsyncMock, MagicMock, patch
from pytest import fixture
from typer.testing import CliRunner
from fam.database.users.models import TransactionTable
from fam.main import app
from tests.utils import input_value

GET_USER_DATABASE_URL = "get_user_database_url"
CHECK_FOR_UPDATE = "check_for_update"
GET_TRANSACTION_BY_DATE_DESC_BANK = "get_transaction_by_date_desc_bank"
GET_ACCOUNT_ID_BY_NAME = "get_account_id_by_name"
GET_ALL_SUBCATEGORY = "get_all_subcategory"
GET_ALL_CLASSIFICATION = "get_all_classification"
CREATE_TRANSACTION = "create_transaction"
COMMAND = ["create", "transaction"]


@fixture
def user_input(transaction_list_form_database) -> list[str]:

    db_transaction: TransactionTable = transaction_list_form_database[0]

    return [
        db_transaction.description,
        db_transaction.product,
        "200.25",
        "20240525",
        db_transaction.bank_name,
        "50",
    ]


@fixture
def mock_is_transaction_auto_classifiable():

    is_transaction_auto_classifiable_patch: str = (
        "fam.command.creating.create.is_transaction_auto_classifiable"
    )

    with patch(is_transaction_auto_classifiable_patch, autospec=True) as mock:
        yield mock


@fixture
def init_mock(
    database_url,
    mock_check_for_update,
    mock_get_user_database_url,
    mock_get_transaction_by_date_desc_bank,
    mock_get_account_id_by_name,
    mock_get_all_subcategory,
    mock_get_all_classification,
    account_from_database,
    subcategory_list_from_database,
    classification_list_from_database,
    mock_create_transaction,
) -> dict[str, MagicMock | AsyncMock]:
    mock_get_user_database_url.return_value = database_url
    mock_check_for_update.return_value = None
    mock_get_transaction_by_date_desc_bank.return_value = None
    mock_get_account_id_by_name.return_value = account_from_database
    mock_get_all_subcategory.return_value = subcategory_list_from_database
    mock_get_all_classification.return_value = classification_list_from_database
    mock_create_transaction.return_value = None

    return {
        "get_user_database_url": mock_get_user_database_url,
        "check_for_update": mock_check_for_update,
        "get_transaction_by_date_desc_bank": mock_get_transaction_by_date_desc_bank,
        "get_account_id_by_name": mock_get_account_id_by_name,
        "get_all_subcategory": mock_get_all_subcategory,
        "get_all_classification": mock_get_all_classification,
        "create_transaction": mock_create_transaction,
    }


def test_create_transaction_when_transaction_exist_in_database(
    runner: CliRunner,
    transaction_list_form_database,
    user_input,
    init_mock,
):
    init_mock[GET_TRANSACTION_BY_DATE_DESC_BANK].return_value = (
        transaction_list_form_database[0]
    )

    input_transaction: str = input_value(user_input)

    result = runner.invoke(
        app,
        COMMAND,
        input=input_transaction,
    )

    init_mock[GET_USER_DATABASE_URL].assert_called_once()
    init_mock[GET_TRANSACTION_BY_DATE_DESC_BANK].assert_called_once()

    assert "The transaction already exists in the database." in result.stdout


def test_create_transaction_when_auto_classification_return_False(
    runner: CliRunner,
    init_mock,
    account_from_database,
    user_input,
):

    account_from_database.id = 2
    account_from_database.name = "expense"

    is_transaction_auto_classifiable_patch: str = (
        "fam.command.creating.create.is_transaction_auto_classifiable"
    )

    with patch(
        is_transaction_auto_classifiable_patch, autospec=True
    ) as mock_is_transaction_classifiable:

        mock_is_transaction_classifiable.return_value = False
        user_input.extend(["expense", "1", "1"])

        result = runner.invoke(
            app,
            COMMAND,
            input=input_value(user_input),
        )

        mock_is_transaction_classifiable.assert_called_once()

    init_mock[GET_TRANSACTION_BY_DATE_DESC_BANK].assert_called_once()
    init_mock[GET_ACCOUNT_ID_BY_NAME].assert_called_once()
    init_mock[GET_ALL_SUBCATEGORY].assert_called_once()
    init_mock[GET_ALL_CLASSIFICATION].assert_called_once()
    init_mock[CREATE_TRANSACTION].assert_called_once()

    db_transaction = init_mock[CREATE_TRANSACTION].call_args[1]
    transaction_table: TransactionTable = db_transaction["transactions"][0]

    assert result.exit_code == 0
    assert transaction_table.account_id == 2
    assert transaction_table.subcategory_id == 1
    assert transaction_table.classification_id == 1


def test_create_transaction_when_get_account_id_by_name_return_none(
    init_mock,
    runner: CliRunner,
    user_input,
    mock_is_transaction_auto_classifiable,
):

    init_mock[GET_ACCOUNT_ID_BY_NAME].return_value = None
    mock_is_transaction_auto_classifiable.return_value = False

    user_input.append("expense")

    result = runner.invoke(app, COMMAND, input=input_value(user_input))

    mock_is_transaction_auto_classifiable.assert_called_once()
    init_mock[GET_ACCOUNT_ID_BY_NAME].assert_called_once()

    assert result.exit_code == 1
    assert "No specified account name was found in the database." in result.stdout


def test_create_transaction_when_subcategory_return_empty_list(
    init_mock, mock_is_transaction_auto_classifiable, runner: CliRunner, user_input
):
    mock_is_transaction_auto_classifiable.return_value = False
    init_mock[GET_ALL_SUBCATEGORY].return_value = []

    user_input.append("expense")

    result = runner.invoke(app, COMMAND, input=input_value(user_input))

    mock_is_transaction_auto_classifiable.assert_called_once()
    init_mock[GET_ALL_SUBCATEGORY].assert_called_once()

    assert result.exit_code == 1


def test_create_transaction_when_auto_classifiable_return_true():
    pass


def test_create_transaction_when_user_refuse_auto_classification():
    pass


def test_create_transaction_when_user_accept_auto_classification():
    pass
