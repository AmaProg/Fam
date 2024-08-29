from pytest import fixture
from typer.testing import CliRunner
from fam.database.users.models import TransactionTable
from fam.main import app
from tests.utils import input_value


@fixture
def user_input(transaction_list_form_database) -> list[str]:

    db_transaction: TransactionTable = transaction_list_form_database[0]

    return [
        db_transaction.description,
        db_transaction.product,
        "200.25",
        "20240525",
        db_transaction.bank_name,
    ]


def test_create_transaction_when_transaction_exist_in_database(
    runner: CliRunner,
    mock_get_user_database_url,
    database_url,
    mock_get_transaction_by_date_desc_bank,
    transaction_list_form_database,
    user_input,
    mock_check_for_update,
):
    mock_get_user_database_url.return_value = database_url
    mock_check_for_update.return_value = 1
    mock_get_transaction_by_date_desc_bank.return_value = (
        transaction_list_form_database[0]
    )

    input_transaction: str = input_value(user_input)

    result = runner.invoke(
        app,
        ["create", "transaction"],
        input=input_transaction,
    )

    mock_get_user_database_url.assert_called_once()
    mock_get_transaction_by_date_desc_bank.assert_called_once()

    assert "The transaction already exists in the database." in result.stdout


def test_create_transaction_when_auto_classification_return_False():
    pass


def test_create_transaction_when_get_account_id_by_name_return_none():
    pass


def test_create_transaction_when_subcategory_return_empty_list():
    pass


def test_create_transaction_when_transaction_was_added_successfully():
    pass


def test_create_transaction_when_auto_classifiable_return_true():
    pass


def test_create_transaction_when_user_refuse_auto_classification():
    pass


def test_create_transaction_when_user_accept_auto_classification():
    pass
