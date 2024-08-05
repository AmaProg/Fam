from typing import Any, List

from command.bank import banker
from command.company import statement


MAIN: List[dict[str, Any]] = [banker.bank_command, statement.statement_command]
