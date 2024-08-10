from pytest import fixture
from unittest.mock import patch, MagicMock


@fixture
def mock_app_cli():
    with patch("fam.cli.app_cli") as mock_app_cli:
        yield mock_app_cli
