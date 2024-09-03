from typing import Any
from typer.testing import CliRunner
from fam.main import app


def test_subcategory_list(
    mock_get_user_session,
    database_url,
    mock_get_all_subcategory,
    subcategory_list_from_database,
    runner: CliRunner,
):

    user_session: dict[str, Any] = {"database_url": database_url}

    mock_get_user_session.return_value = user_session
    mock_get_all_subcategory.return_value = subcategory_list_from_database

    result = runner.invoke(app, ["subcategory", "list"])

    mock_get_user_session.assert_called()
    mock_get_all_subcategory.assert_called()

    assert "1: Loyer (Habitation)".lower() in result.stdout.lower()
