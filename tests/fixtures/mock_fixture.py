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
