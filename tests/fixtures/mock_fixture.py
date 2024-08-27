from pathlib import Path
from unittest.mock import patch
from pytest import fixture


@fixture
def mock_read_yaml_file():
    with patch("fam.system.file.File.read_yaml_file", autospec=True) as mock:
        yield mock


@fixture
def mock_save_yaml_file():
    with patch("fam.system.file.File.save_yaml_file", autospec=True) as mock:
        yield mock


@fixture
def mock_init_file_exists():
    # Utilise un patch pour simuler que `init_file.exists()` retourne True
    with patch.object(Path, "exists", return_value=True):
        yield


@fixture
def mock_get_account_id_by_name():
    with patch(
        "fam.database.users.services.get_account_id_by_name", autospec=True
    ) as mock:
        yield mock


@fixture
def mock_get_transaction_by_account_id():
    with patch(
        "fam.database.users.services.get_transaction_by_account_id", autospec=True
    ) as mock:
        yield mock
