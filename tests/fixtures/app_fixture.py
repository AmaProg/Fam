from pathlib import Path
from unittest.mock import patch
from pytest import fixture
from tempfile import TemporaryDirectory
from fam.main import app
from typer.testing import CliRunner
from fam.cli import app_cli


@fixture
def mock_app_cli():
    with patch("fam.cli.app_cli") as mock_app_cli:
        yield mock_app_cli


@fixture
def create_app_temp_dir():
    with TemporaryDirectory() as temp_dir:
        temp_path: Path = Path(temp_dir)
        app_name = "Fam"
        app_dir: Path = temp_path / "AppData" / "Local" / app_name

        yield app_dir


@fixture
def init_app_dir(create_app_temp_dir):
    app_dir_path: Path = Path(create_app_temp_dir)
    temp_dir: Path = app_dir_path.parent.parent.parent

    app_folder: Path = temp_dir / "static" / "template" / "app"
    app_folder.mkdir(parents=True, exist_ok=True)
    init_file_path = app_folder / "init"
    init_file_path.touch()

    with patch("fam.action.app_cli") as mock_app_cli:

        mock_app_cli.directory.app_dir = app_dir_path.as_posix()
        mock_app_cli.directory.exe = temp_dir.as_posix()
        mock_app_cli.startup.return_value = None
        mock_app_cli.directory.copy_folder = app_cli.directory.copy_folder

        runner: CliRunner = CliRunner()

        result = runner.invoke(app, ["init"])

        yield app_dir_path
