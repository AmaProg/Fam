from os import name
from typing import Sequence
from sqlalchemy.orm import Session
import typer

from fam.command import utils
from fam.command.utils import build_choice, prompt_choice
from fam.database.users import service
from fam.database.users.models import (
    AccountNicknameTable,
    AccountTable,
    ClassificationTable,
    SubCategoryTable,
    TransactionTable,
)
from fam.database.users.schemas import CreateTransactionModel
from fam.enums import (
    BankEnum,
    FinancialAccountEnum,
    FinancialProductEnum,
    InstitutionEnum,
    TransactionTypeEnum,
    AccountSectionEnum,
)
from fam.utils import fprint, fprint_panel, is_empty_list


def create_new_account_nickname(
    bank_name: str,
    account_type_name: str,
    nickname: str,
    db: Session,
) -> None:

    service.account_nickname.create_nickname_by_bank_account_type_nickname(
        bank_name=bank_name,
        account=account_type_name,
        nickname=nickname,
        db=db,
    )


def create_new_transaction(
    db: Session,
    desc: str,
    product: FinancialAccountEnum,
    amount: float,
    date_value: int,
    bank: InstitutionEnum,
    pay_proportion: float,
    transaction_type: TransactionTypeEnum,
) -> None:

    # Retrieve and display the account nickname to the user
    db_account_nickname: Sequence[AccountNicknameTable] = (
        service.account_nickname.get_account_nickname(db)
    )

    if not db_account_nickname:
        fprint(
            "Please create an account nickname with the create account-nickname command."
        )
        raise typer.Abort()

    nickname_dict, nickname_choice = build_choice(db_account_nickname, "nickname")

    while True:

        nickname_id: int = prompt_choice(nickname_choice, "Select the nickname", "")
        nickname: AccountNicknameTable = nickname_dict.get(nickname_id, None)

        if nickname is not None:
            break

    # Check if the transaction already exists in the database

    transaction_model: CreateTransactionModel = CreateTransactionModel(
        account_id=0,
        amount=amount,
        bank_name=bank.value,
        classification_id=0,
        date=date_value,
        description=desc,
        hash="",
        payment_proportion=(pay_proportion / 100),
        product=product.value,
        subcategory_id=0,
        transaction_type=transaction_type.value,
        account_nickname_id=nickname.id,
    )

    hash_id: str = utils.generate_transaction_hash(
        transaction=transaction_model,
    )

    transaction_model.hash = hash_id

    db_transaction: TransactionTable = service.transaction.get_transaction_by_hash(
        db=db,
        hash=hash_id,
    )

    if db_transaction is not None:
        fprint("The transaction already exists in the database.")
        raise typer.Abort()

    # Show the account name
    account_enum: AccountSectionEnum = typer.prompt(
        type=AccountSectionEnum,
        text=f"Please select an account ({[section.value for section in AccountSectionEnum]})",
    )

    db_account: AccountTable = service.account.get_account_id_by_name(
        db=db,
        account_name=account_enum.value,
    )

    if db_account is None:
        fprint_panel(
            msg="No specified account name was found in the database.",
            title="Account name error",
            color="red",
        )
        raise typer.Abort()

    db_subcategory, db_classification = (
        service.utils.get_subcategory_and_classification(db)
    )

    # # Show the subcategory
    # db_subcategory: Sequence[SubCategoryTable] = service.subcategory.get_subcategories(
    #     db
    # )

    if not db_subcategory:
        fprint(
            "Please create one or more subcategories before using the [green]"
            "create transaction"
            "[/green] command."
        )
        raise typer.Abort()

    _, subcategory_choice = build_choice(db_subcategory, "categogy")

    subcategory_id: int = prompt_choice(
        subcategory_choice,
        "Select the subcategory",
        transaction_model.description,
    )

    # # Show the classification
    # db_classification: Sequence[ClassificationTable] = (
    #     service.classification.get_all_classification(db)
    # )

    _, class_choice = build_choice(db_classification)

    cls_id: int = prompt_choice(
        class_choice,
        "Select the classification",
        transaction_model.description,
    )

    transaction_model.account_id = db_account.id
    transaction_model.subcategory_id = subcategory_id
    transaction_model.classification_id = cls_id

    # Add the transaction to the database

    service.transaction.create_one_transaction(db=db, transaction=transaction_model)
