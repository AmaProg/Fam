from pathlib import Path
import pytest
from unittest.mock import patch, MagicMock
from tempfile import TemporaryDirectory

from typer.testing import CliRunner

from fam.cli import AppCli, app_cli
from fam.main import app  # Remplacez par le nom de votre module


@pytest.fixture
def runner() -> CliRunner:
    return CliRunner()


@patch("fam.action.app_cli", autospec=True)
def test_create_app_dir(mock_app_cli_instance: MagicMock, runner: CliRunner):

    mock_app_cli: MagicMock = mock_app_cli_instance
    with TemporaryDirectory() as temp_dir:

        temp_path: Path = Path(temp_dir)
        app_name = "Fam"
        app_dir: Path = temp_path / "AppData" / "Local" / app_name
        app_name = "Fam"

        # Créez le dossier `app` et le fichier `init` dans ce dossier
        app_folder = temp_path / "static" / "template" / "app"
        app_folder.mkdir(parents=True, exist_ok=True)
        init_file_path = app_folder / "init"
        init_file_path.touch()  # Créez un fichier `init` vide

        mock_app_cli.directory.app_dir = app_dir.as_posix()
        mock_app_cli.directory.exe = temp_path.as_posix()
        mock_app_cli.startup.return_value = None
        mock_app_cli.directory.copy_folder = app_cli.directory.copy_folder

        result = runner.invoke(app, ["init"])

        assert result.exit_code == 0
        assert "The workspace was successfully created" in result.stdout
