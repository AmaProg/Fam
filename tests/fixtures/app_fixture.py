from pathlib import Path
from typing import Any
from pytest import fixture
from tempfile import TemporaryDirectory
import shutil

from fam.database.users.schemas import CreateTransactionBM


@fixture
def create_temp_dir():

    with TemporaryDirectory(
        prefix="fam_", suffix="_test", ignore_cleanup_errors=True
    ) as secure_temp:
        yield Path(secure_temp)


@fixture
def app_dir_path():
    app_name: str = "FAM"
    return f"AppData/Local/{app_name}"


@fixture
def prepare_app(create_temp_dir, app_dir_path):
    temp_path: Path = create_temp_dir
    app_path: Path = temp_path / app_dir_path

    src: str = r"src\fam\static\template\app"
    dest: str = app_path.as_posix()

    shutil.copytree(src, dest)

    return temp_path, app_path


@fixture
def transaction_yaml_file(
    transaction_base_model_bmo_bank,
) -> dict[str, list[dict[str, Any]]]:

    old_trans: CreateTransactionBM = transaction_base_model_bmo_bank

    old_trans.description = "IGA Epicerie"
    old_trans.amount = 520.20

    rule_data: dict[str, list[dict[str, Any]]] = {"rule": [old_trans.model_dump()]}

    return rule_data


# from pathlib import Path

# from unittest.mock import patch

# from tempfile import TemporaryDirectory
# from fam.main import app
# from typer.testing import CliRunner
# from fam.cli import app_cli


# @fixture
# def mock_app_cli():
#     with patch("fam.cli.app_cli") as mock_app_cli:
#         yield mock_app_cli


# @fixture
# def create_app_temp_dir():
#     with TemporaryDirectory() as temp_dir:
#         temp_path: Path = Path(temp_dir)
#         app_name = "Fam"
#         app_dir: Path = temp_path / "AppData" / "Local" / app_name

#         yield app_dir


# @fixture
# def init_app(create_app_temp_dir):
#     app_dir_path: Path = Path(create_app_temp_dir)
#     temp_dir: Path = app_dir_path.parent.parent.parent

#     src: str = "./tests/fixtures/app"

#     shutil.copytree(src, app_dir_path.as_posix())

#     print("")


# @fixture
# def init_app_dir(create_app_temp_dir):
#     app_dir_path: Path = Path(create_app_temp_dir)
#     temp_dir: Path = app_dir_path.parent.parent.parent

#     app_folder: Path = temp_dir / "static" / "template" / "app"
#     app_folder.mkdir(parents=True, exist_ok=True)
#     init_file_path = app_folder / "init"
#     init_file_path.touch()

#     with patch("fam.action.app_cli") as mock_app_cli:

#         mock_app_cli.directory.app_dir = app_dir_path.as_posix()
#         mock_app_cli.directory.exe = temp_dir.as_posix()
#         mock_app_cli.startup.return_value = None
#         mock_app_cli.directory.copy_folder = app_cli.directory.copy_folder

#         runner: CliRunner = CliRunner()

#         result = runner.invoke(app, ["init"])

#         yield app_dir_path
