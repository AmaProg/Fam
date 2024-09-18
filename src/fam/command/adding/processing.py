from pandas import DataFrame
from sqlalchemy.orm import Session
import typer
from fam.bank.statement import BankStatement
from fam.command.adding.validation import is_auto_categorized
from fam.command.utils import generate_transaction_hash, prompt_choice
from fam.database.users import service
from fam.database.users.models import SubCategoryTable, TransactionTable
from fam.database.users.schemas import CreateTransactionModel
from fam.enums import BankEnum, FinancialProductEnum
from fam.utils import fprint


def categorize_transaction(
    bank: BankEnum,
    df: DataFrame,
    product: FinancialProductEnum,
    nickname_id: int,
    db: Session,
    subcat_choice: list[str],
    class_choice: list[str],
    subcat_dict: dict[int, SubCategoryTable],
) -> list[TransactionTable]:

    # Standardize bank statement
    bank_statement = BankStatement()

    transaction_list = bank_statement.standardize_statement(
        bank_name=bank,
        csv_data=df,
        product=product,
    )

    # Create a list for transactionTable
    transaction_table_list: list[TransactionTable] = []

    for transaction in transaction_list:

        transaction.bank_name = bank.value
        transaction.account_nickname_id = nickname_id
        transaction.hash = generate_transaction_hash(transaction)

        # Check if the transaction already exists in the database
        db_transaction: TransactionTable = service.transaction.get_transaction_by_hash(
            db=db,
            hash=transaction.hash,
        )

        if db_transaction is not None:
            msg: str = (
                f"The following description {transaction.description} already exists."
            )
            fprint(msg)
            continue

        # Check if the transaction is auto-categorized
        result, auto_transaction = is_auto_categorized(
            db=db,
            transaction_model=transaction,
            transaction_table_list=transaction_table_list,
        )

        if result:
            transaction_categorize: CreateTransactionModel = (
                categorize_transaction_automatically(
                    auto_transaction=auto_transaction,
                    transaction_model=transaction,
                )
            )

            transaction_table_list.append(
                TransactionTable(**transaction_categorize.model_dump())
            )
            msg: str = (
                f"Transaction {transaction_categorize.description} has been automatically classified."
            )
            fprint(msg)
            continue

        # If not auto-categorized, classify the transaction manually
        new_transaction: CreateTransactionModel | None = (
            categorize_transaction_manually(
                class_choice=class_choice,
                subcat_choice=subcat_choice,
                subcat_dict=subcat_dict,
                transaction_model=transaction,
            )
        )

        if new_transaction is None:
            msg: str = f"The transaction has not been categorized."
            fprint(msg, color="red")
            continue

        transaction_table_list.append(TransactionTable(**new_transaction.model_dump()))

    # Save the data to the database
    return transaction_table_list


def categorize_transaction_automatically(
    transaction_model: CreateTransactionModel,
    auto_transaction: TransactionTable,
) -> CreateTransactionModel:

    # during the automatic categorization the date, amount, transaction
    # type, nickname id, bank name, pay ratio and de description cannot be changed

    transaction_model.account_id = auto_transaction.account_id
    transaction_model.classification_id = auto_transaction.classification_id
    transaction_model.subcategory_id = auto_transaction.subcategory_id
    transaction_model.auto_categorize = auto_transaction.auto_categorize

    return transaction_model


def categorize_transaction_manually(
    transaction_model: CreateTransactionModel,
    subcat_choice: list[str],
    class_choice: list[str],
    subcat_dict: dict[int, SubCategoryTable],
) -> CreateTransactionModel | None:

    subcat_id: int = prompt_choice(
        subcat_choice,
        "Select a category",
        transaction_model.description,
    )

    if not subcat_id:
        return None

    # show the message to select a classification.
    cls_id: int = prompt_choice(
        class_choice,
        "Select a category",
        transaction_model.description,
    )

    if not cls_id:
        return None

    subcategory_table: SubCategoryTable = subcat_dict.get(subcat_id, None)

    if not subcategory_table:
        raise typer.Abort()

    while True:

        pay_ratio: float = typer.prompt(
            type=float,
            text="What is the ratio payement (min: 0 and max: 100 %)",
        )

        if pay_ratio >= 0 and pay_ratio <= 100:
            break

    transaction_model.subcategory_id = subcat_id
    transaction_model.classification_id = cls_id
    transaction_model.account_id = subcategory_table.category.account_id
    transaction_model.payment_proportion = pay_ratio / 100

    if typer.confirm(
        "Do you want the next time you see the transaction to be filed automatically?",
        err=True,
    ):
        transaction_model.auto_categorize = True
        fprint("The transaction has been successfully classified.")

    return transaction_model
