# from pathlib import Path
# import pytest
# from unittest.mock import patch, MagicMock
# from tempfile import TemporaryDirectory

# from typer.testing import CliRunner


# from fam.cli import app_cli
# from fam.main import app  # Remplacez par le nom de votre module


# @patch("fam.action.app_cli", autospec=True)
# def test_create_app_dir(mock_app_cli_instance: MagicMock, runner: CliRunner):

#     mock_app_cli: MagicMock = mock_app_cli_instance
#     with TemporaryDirectory() as temp_dir:

#         temp_path: Path = Path(temp_dir)
#         app_name = "Fam"
#         app_dir: Path = temp_path / "AppData" / "Local" / app_name

#         # Créez le dossier `app` et le fichier `init` dans ce dossier
#         app_folder = temp_path / "static" / "template" / "app"
#         app_folder.mkdir(parents=True, exist_ok=True)
#         init_file_path = app_folder / "init"
#         init_file_path.touch()  # Créez un fichier `init` vide

#         mock_app_cli.directory.app_dir = app_dir.as_posix()
#         mock_app_cli.directory.exe = temp_path.as_posix()
#         mock_app_cli.startup.return_value = None
#         mock_app_cli.directory.copy_folder = app_cli.directory.copy_folder

#         result = runner.invoke(app, ["init"])

#         assert result.exit_code == 0
#         assert "The app was successfully created" in result.stdout


# def test_reset_app_dir_by_force(runner: CliRunner, init_app_dir):

#     app_dir_path: Path = init_app_dir
#     temp_dir: Path = app_dir_path.parent.parent.parent
#     database: Path = app_dir_path / "database.db"
#     database.touch()

#     with patch("fam.main.app_cli") as mock_app_cli:
#         mock_app_cli.directory.app_dir = app_dir_path.as_posix()
#         mock_app_cli.directory.exe = temp_dir.as_posix()
#         mock_app_cli.startup.return_value = None
#         mock_app_cli.directory.copy_folder = app_cli.directory.copy_folder

#         result = runner.invoke(app, ["reset", "--force"])

#         assert result.exit_code == 0
#         assert database.exists() == False
#         assert app_dir_path.exists() == True


# def test_reset_app_dir_by_confirming_yes(runner: CliRunner, init_app_dir):
#     app_dir_path: Path = init_app_dir
#     temp_dir: Path = app_dir_path.parent.parent.parent
#     database: Path = app_dir_path / "database.db"
#     database.touch()

#     with patch("fam.main.app_cli") as mock_app_cli:
#         mock_app_cli.directory.app_dir = app_dir_path.as_posix()
#         mock_app_cli.directory.exe = temp_dir.as_posix()
#         mock_app_cli.startup.return_value = None
#         mock_app_cli.directory.copy_folder = app_cli.directory.copy_folder

#         result = runner.invoke(app, ["reset"], input="y\n")

#         assert result.exit_code == 0
#         assert database.exists() == False
#         assert app_dir_path.exists() == True


# def test_reset_app_dir_by_confirming_no(runner: CliRunner, init_app_dir):
#     app_dir_path: Path = init_app_dir
#     temp_dir: Path = app_dir_path.parent.parent.parent
#     database: Path = app_dir_path / "database.db"
#     database.touch()

#     with patch("fam.main.app_cli") as mock_app_cli:
#         mock_app_cli.directory.app_dir = app_dir_path.as_posix()
#         mock_app_cli.directory.exe = temp_dir.as_posix()
#         mock_app_cli.startup.return_value = None
#         mock_app_cli.directory.copy_folder = app_cli.directory.copy_folder

#         result = runner.invoke(app, ["reset"], input="N\n")

#         assert result.exit_code == 0
#         assert database.exists() == True
#         assert "Aborted" in result.stdout


# def test_delete_app_dir_by_confirming_yes(runner: CliRunner, init_app_dir):
#     app_dir_path: Path = init_app_dir
#     temp_dir: Path = app_dir_path.parent.parent.parent

#     with patch("fam.main.app_cli") as mock_app_cli:
#         mock_app_cli.directory.app_dir = app_dir_path.as_posix()
#         mock_app_cli.directory.exe = temp_dir.as_posix()
#         mock_app_cli.startup.return_value = None
#         mock_app_cli.directory.copy_folder = app_cli.directory.copy_folder

#         result = runner.invoke(app, ["delete", "--app"], input="y\n")

#         assert result.exit_code == 0
#         assert app_dir_path.exists() == False
#         assert "The app was successfully deleted" in result.stdout


# def test_delete_app_dir_by_confirming_no(runner: CliRunner, init_app_dir):
#     app_dir_path: Path = init_app_dir
#     temp_dir: Path = app_dir_path.parent.parent.parent

#     with patch("fam.main.app_cli") as mock_app_cli:
#         mock_app_cli.directory.app_dir = app_dir_path.as_posix()
#         mock_app_cli.directory.exe = temp_dir.as_posix()
#         mock_app_cli.startup.return_value = None
#         mock_app_cli.directory.copy_folder = app_cli.directory.copy_folder

#         result = runner.invoke(app, ["delete", "--app"], input="N\n")

#         assert result.exit_code == 1
#         assert app_dir_path.exists() == True
#         assert "Aborted" in result.stdout
