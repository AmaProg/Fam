from typer.testing import CliRunner
from fam.database.users.models import AccountTable
from fam.main import app


def test_expense_command_in_normale_execution(
    runner: CliRunner,
    mock_init_file_exists,
    transaction_list_form_database,
    mock_get_account_id_by_name,
    mock_get_transaction_by_account_id,
):

    expense_account: AccountTable = AccountTable()
    expense_account.id = 2

    mock_get_account_id_by_name.return_value = expense_account
    mock_get_transaction_by_account_id.return_value = transaction_list_form_database

    result = runner.invoke(app, ["expense", "build"])

    mock_get_account_id_by_name.assert_called()
    mock_get_transaction_by_account_id.assert_called()

    assert result.exit_code == 0
    assert "Habitation" in result.stdout
    assert "800" in result.stdout
