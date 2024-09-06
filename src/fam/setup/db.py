from copy import copy
from fam.database.users.models import AccountTable, ClassificationTable
from fam.database.users.schemas import AccountSchemas, ClassifySchemas
from fam.database.users import service
from sqlalchemy.orm import Session


def init_account_table(db: Session) -> list[AccountTable]:
    account_name: list[str] = ["income", "expense", "asset", "passive"]
    account_desc: list[str] = [
        "Income Acoount",
        "Expense account.",
        "Asset account.",
        "Passive account.",
    ]

    account_schemas_list: list[AccountSchemas] = []

    for idx, name in enumerate(account_name):
        account_schemas: AccountSchemas = AccountSchemas(
            name=name, description=account_desc[idx]
        )

        account_schemas_list.append(copy(account_schemas))

    return service.account.create_account_by_account_model(
        db=db,
        account_schemas_list=account_schemas_list,
    )


def init_classification_table(db: Session) -> None:
    class_name: list[str] = ["personal", "family"]

    class_schemas: list[ClassifySchemas] = []

    for name in class_name:
        classify: ClassifySchemas = ClassifySchemas(
            name=name,
        )

        class_schemas.append(copy(classify))

    service.classification.create_new_classification(
        db=db,
        classifies=class_schemas,
    )


def init_category_table(db: Session) -> None:
    pass


def init_subcategory_table() -> None:
    pass
