from pathlib import Path
from unittest.mock import patch
from fam.command.adding.action import get_transaction_rule_file


def test_get_transaction_rule_path():
    database_url: Path = Path(
        "sqlite:///C:/Users/user_name/AppData/Local/Financial_Advisor_for_Me/users/b5d49fb06b704b55bc4a9188b972ed78/db/user_database.db"
    )
    user_dir: Path = Path(
        r"C:\Users\user_name\AppData\Local\Financial_Advisor_for_Me\users\b5d49fb06b704b55bc4a9188b972ed78"
    )

    trans_rule_file: Path = get_transaction_rule_file(database_url.as_posix())

    assert trans_rule_file.as_posix() == (user_dir / "transaction_rule.yaml").as_posix()


def test_add_transaction_to_rule_file():

    with patch("fam.command.adding.action.File.read_yaml_file") as mock_read_yaml_file:
        mock_read_yaml_file.read_yaml_file.return_value = None
