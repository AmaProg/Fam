from typing import Any
import typer
from typer.testing import CliRunner
from unittest.mock import patch
from tests.utils import input_value
from fam.main import app


def test_user_login(runner: CliRunner, user_login, prepare_database):

    email, pwd = user_login

    input_login: str = input_value([email, pwd])

    config: dict[str, Any] = prepare_database

    with patch("fam.database.db.get_db_app") as mock_db_app:
        with patch("fam.cli.typer", spec=typer) as mock_typer:
            mock_db_app.return_value = config["db_path"]
            mock_typer.get_app_dir.return_value = config["app_dir"]

            result = runner.invoke(app, ["login"], input=input_login)

    assert result.exit_code == 0
    assert "Fam: Connection successful." in result.stdout


def test_user_login_with_invalid_email(runner: CliRunner, user_login, prepare_database):

    email, pwd = user_login

    input_login: str = input_value(["Dave", pwd])

    config: dict[str, Any] = prepare_database

    with patch("fam.database.db.get_db_app") as mock_db_app:
        with patch("fam.cli.typer", spec=typer) as mock_typer:
            mock_db_app.return_value = config["db_path"]
            mock_typer.get_app_dir.return_value = config["app_dir"]

            result = runner.invoke(app, ["login"], input=input_login)

    assert result.exit_code == 1
    assert "Fam: The password or username is invalid." in result.stdout
    assert "Aborted" in result.stdout


def test_user_login_with_invalid_password(
    runner: CliRunner, user_login, prepare_database
):

    email, pwd = user_login

    input_login: str = input_value([email, "987456321"])

    config: dict[str, Any] = prepare_database

    with patch("fam.database.db.get_db_app") as mock_db_app:
        with patch("fam.cli.typer", spec=typer) as mock_typer:
            mock_db_app.return_value = config["db_path"]
            mock_typer.get_app_dir.return_value = config["app_dir"]

            result = runner.invoke(app, ["login"], input=input_login)

    assert result.exit_code == 1
    assert "Fam: The password or username is invalid." in result.stdout
    assert "Aborted" in result.stdout
