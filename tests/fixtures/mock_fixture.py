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


@fixture
def mock_get_user_session():
    with patch("fam.auth.get_user_session", autospec=True) as mock:
        yield mock


@fixture
def mock_get_all_subcategory():
    with patch(
        "fam.database.users.services.get_all_subcategory", autospec=True
    ) as mock:
        yield mock


@fixture
def mock_get_user_database_url():
    with patch("fam.auth.get_user_database_url", autospec=True) as mock:
        yield mock


@fixture
def mock_get_transaction_by_date_desc_bank():
    with patch(
        "fam.database.users.services.get_transaction_by_date_desc_bank", autospec=True
    ) as mock:
        yield mock


@fixture
def mock_is_transaction_classifiable():
    with patch(
        "fam.command.adding.action.is_transaction_auto_classificable", autospec=True
    ) as mock:
        yield mock


@fixture
def mock_classify_transaction_auto():
    with patch(
        "fam.command.adding.action.classify_transaction_auto", autospec=True
    ) as mock:
        yield mock


@fixture
def mock_create_transaction():
    with patch("fam.database.users.services.create_transaction", autospec=True) as mock:
        yield mock


@fixture
def mock_get_all_classification():
    with patch(
        "fam.database.users.services.get_all_classification", autospec=True
    ) as mock:
        yield mock


@fixture
def mock_check_for_update():
    with patch("fam.core.check_for_update") as db:
        yield db
