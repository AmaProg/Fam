from typing import Any, List

from fam.command import bank, invoice
from fam.command.adding import add
from fam.command.charge import expense
from fam.command.creating import create
from fam.command.subcategory import subcategory


MAIN: List[dict[str, Any]] = [
    create.create_command,
    expense.expense_command,
    bank.bank_command,
    invoice.invoice_command,
    add.add_command,
    subcategory.subcategory_command,
]
