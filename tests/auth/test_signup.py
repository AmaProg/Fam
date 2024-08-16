import typer
from typer.testing import CliRunner
from unittest.mock import patch, PropertyMock
from fam.main import app


def test_create_new_user(prepare_app, runner: CliRunner):

    fname: str = "Paul"
    lname: str = "Walker"
    pwd = cfm_pwd = "123456789"

    input_data: str = f"{fname}\n{lname}\n{pwd}\n{cfm_pwd}\n"

    temp_dir, app_dir = prepare_app

    with patch("fam.database.db.get_db_app") as mock_db_app:
        with patch("fam.cli.typer", spec=typer) as mock_typer:
            mock_db_app.return_value = app_dir / "auth.db"
            mock_typer.get_app_dir.return_value = app_dir.as_posix()

            result = runner.invoke(app, ["signup"], input=input_data)

    assert result.exit_code == 0
    assert "Your account has been successfully created." in result.stdout
