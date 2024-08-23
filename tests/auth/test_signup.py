import typer
from typer.testing import CliRunner
from unittest.mock import patch, PropertyMock
from fam.main import app


def test_create_new_user(prepare_app, runner: CliRunner):

    email: str = "Walker"
    pwd = cfm_pwd = "123456789"

    input_data: str = f"{email}\n{pwd}\n{cfm_pwd}\n"

    temp_dir, app_dir = prepare_app

    with patch("fam.database.db.get_db_app") as mock_db_app:
        with patch("fam.cli.typer", spec=typer) as mock_typer:
            mock_db_app.return_value = f"sqlite:///{(app_dir / "auth.db").as_posix()}"
            mock_typer.get_app_dir.return_value = app_dir.as_posix()

            result = runner.invoke(app, ["signup"], input=input_data)

    assert result.exit_code == 0
    assert "Fam: The new database was successfully created." in result.stdout
    assert "Fam: Your account has been successfully created." in result.stdout

def test_signup_when_user_already_exists_in_database(prepare_app, runner: CliRunner):

    email: str = "Walker"
    pwd = cfm_pwd = "123456789"

    input_data: str = f"{email}\n{pwd}\n{cfm_pwd}\n"

    temp_dir, app_dir = prepare_app

    with patch("fam.database.db.get_db_app") as mock_db_app:
        with patch("fam.cli.typer", spec=typer) as mock_typer:
            mock_db_app.return_value = f"sqlite:///{(app_dir / "auth.db").as_posix()}"
            mock_typer.get_app_dir.return_value = app_dir.as_posix()

            runner.invoke(app, ["signup"], input=input_data)
            result = runner.invoke(app, ["signup"], input=input_data)

    assert result.exit_code == 0
    assert "Fam: The user already exists." in result.stdout
    assert "Aborted" in result.stdout
