from typing import Any, List

from fam.command import create, expense, bank, invoice
from fam.command.adding import add


MAIN: List[dict[str, Any]] = [
    create.create_command,
    expense.expense_command,
    bank.bank_command,
    invoice.invoice_command,
    add.add_command,
]
