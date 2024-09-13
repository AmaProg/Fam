import json
import hashlib
from typing import Any
import typing_extensions


@typing_extensions.deprecated("Use from fam.command.utils", category=None)
def generate_transaction_hash(transaction: dict[Any, Any]):

    unique_string = json.dumps(transaction, sort_keys=True)

    return hashlib.md5(unique_string.encode()).hexdigest()
