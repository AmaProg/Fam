from typing import Any, List

from fam.command import expense, bank, invoice
from fam.command.adding import add
from fam.command.creating import create


MAIN: List[dict[str, Any]] = [
    create.create_command,
    expense.expense_command,
    bank.bank_command,
    invoice.invoice_command,
    add.add_command,
]
