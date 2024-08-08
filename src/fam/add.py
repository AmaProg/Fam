from typing import Any, List

from command import create, expense, bank, invoice


MAIN: List[dict[str, Any]] = [
    create.create_command,
    expense.expense_command,
    bank.bank_command,
    invoice.invoice_command,
]
