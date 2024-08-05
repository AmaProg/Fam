from typing import Any, List

from command.bank import banker
from command.company import statement
from command.budget import financial


MAIN: List[dict[str, Any]] = [
    banker.bank_command,
    statement.statement_command,
    financial.financial_command,
]
