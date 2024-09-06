from copy import copy
from typing import Any, Sequence
from typing_extensions import Annotated
from typer import Typer

from rich import print
import typer

from fam import auth
from fam.bank.constants import BANK_INST, BANK_INSTANCE_TYPE
from fam.command.adding.action import (
    classify_transaction_auto,
    is_transaction_auto_classifiable,
)
from fam.database.db import DatabaseType, get_db
from fam.database.users.models import (
    AccountTable,
    BankingInstitutionTable,
    CategoryTable,
    ClassificationTable,
    SubCategoryTable,
    TransactionTable,
)
from fam.database.users.schemas import (
    CategoryBM,
    ClassifySchemas,
    CreateSubCategory,
    CreateTransactionBM,
)
from fam.enums import (
    AccountSectionEnum,
    AccountTypeEnum,
    BankEnum,
    FinancialProductEnum,
    TransactionTypeEnum,
)
from fam.utils import fAborted, fprint, fprint_panel, is_empty_list
from fam.database.users import service, services as user_services
from fam.command.utils import build_choice, date_to_timestamp, prompt_choice

app = Typer(
    help="Creates bank accounts and expense or income categories.",
    no_args_is_help=True,
)

create_command: dict[str, Any] = {"app": app, "name": "create"}


@app.command(
    help="Allows you to create expense or income categories.",
)
def category(
    name: Annotated[
        str,
        typer.Option(
            "--name",
            "-n",
            help="Category name.",
            prompt="What is the name of the category?",
        ),
    ] = None,
    account_type: Annotated[
        AccountSectionEnum,
        typer.Option(
            "--account",
            "-a",
            help="Name of the account which groups the categories.",
            case_sensitive=False,
            show_choices=True,
            prompt="What is the category type?",
        ),
    ] = None,
    desc: Annotated[
        str,
        typer.Option(
            "--desc",
            "-d",
            help="Description of the category.",
            prompt="Give a description to the category",
            show_choices=False,
        ),
    ] = "",
):

    try:

        # Get session file
        session = auth.get_user_session()

        database_url: str = session["database_url"]

        with get_db(database_url, DatabaseType.USER) as db:

            # Check if the category is alredy in the database
            cat_table: CategoryTable | None = user_services.get_category_by_name(
                db,
                name,
            )

            if cat_table is not None:
                fprint("The category is already present.")
                raise typer.Abort()

            # add category
            account_table: AccountTable | None = user_services.get_account_id_by_name(
                db, account_type.value
            )

            if account_table is None:
                raise typer.Abort()

            cat_base_model: CategoryBM = CategoryBM(
                name=name,
                description=desc,
                account_id=account_table.id,
            )

            user_services.create_new_category(db, cat_base_model)

        # print success added category
        fprint("The category was added successfully.")

    except typer.Abort as e:
        fAborted()

    except Exception as e:
        print(e)

    pass


@app.command()
def subcategory():
    try:
        # Get user session
        session = auth.get_user_session()

        database_url = session["database_url"]

        with get_db(db_path=database_url, db_type=DatabaseType.USER) as db:

            # Get all category and build choice
            cat: Sequence[CategoryTable] = user_services.get_all_category(db)

            if cat is None or len(cat) == 0:
                fprint("Please create a category before adding a bank statement.")
                raise typer.Abort

            cat_dict, cat_choice = build_choice(cat)

            typer.echo(cat_choice)
            cat_id = typer.prompt(type=int, text="\nSelect de category")

            category_table: CategoryTable | None = cat_dict.get(cat_id, None)

            ans: str = typer.prompt(
                type=str, text="Please enter the subcategories separating them with (,)"
            )

            list_sub_cat: list = ans.split(",")

            subcategories: list[SubCategoryTable] = []

            for idx, sub in enumerate(list_sub_cat):
                new_sub_cat: CreateSubCategory = CreateSubCategory(
                    name=sub,
                    category_id=category_table.id,  # type: ignore
                )

                subcategories.append(SubCategoryTable(**copy(new_sub_cat.model_dump())))

            # Save category in the database
            user_services.create_subcategory(db, subcategories)

        fprint("The subcategories have been added successfully.")

    except FileNotFoundError:
        fprint("Please log in")
        fAborted()

    except typer.Abort:
        fAborted()

    except Exception as e:
        fprint(e)


@app.command(
    help="Allows you to add new transactions manually.",
)
def transaction(
    description: Annotated[
        str,
        typer.Option(
            "--description",
            "-d",
            help="Description of the transaction.",
            prompt="Please enter a description.",
        ),
    ] = "",
    product: Annotated[
        FinancialProductEnum,
        typer.Option(
            "--product",
            "-p",
            help="Financial product of the transaction.",
            prompt="Please enter a financial product.",
            show_choices=True,
            case_sensitive=True,
        ),
    ] = None,
    amount: Annotated[
        float,
        typer.Option(
            "--amount",
            "-a",
            help="Transaction amount.",
            prompt="Please enter an amount.",
        ),
    ] = 0,
    date: Annotated[
        str,
        typer.Option(
            "--date",
            help="Transaction date.",
            prompt="Please enter the transaction date.",
        ),
    ] = "",
    bank: Annotated[
        BankEnum,
        typer.Option(
            "--bank",
            "-b",
            help="The name of the bank which generated the transaction.",
            prompt="Please enter bank name",
            show_choices=True,
        ),
    ] = None,
    pay_proportion: Annotated[
        float,
        typer.Option(
            "--pay-proportion",
            help="Allows you to define the portion that you will pay on the invoice in %.",
            prompt="How much do you pay on this bill",
            show_choices=True,
            max=100,
            min=1,
        ),
    ] = None,
    transaction_type: Annotated[
        TransactionTypeEnum,
        typer.Option(
            "--transaction_type",
            "-t",
            help="",
            prompt="Please indicate the transaction type: Withdrawal (debit) Deposit (credit)",
            show_choices=True,
        ),
    ] = None,
):
    # Get the user database url
    database_url: str = auth.get_user_database_url()

    with get_db(db_path=database_url, db_type=DatabaseType.USER) as db:

        # Create a new transaction
        new_transaction: CreateTransactionBM = CreateTransactionBM(
            description=description.upper(),
            product=product.value,
            amount=abs(amount),
            date=date_to_timestamp(date),
            bank_name=bank,
            payment_proportion=(pay_proportion / 100),
            account_id=0,
            classification_id=0,
            subcategory_id=0,
            transaction_type=transaction_type.value,
        )

        # check if the transaction is alredy in the database
        db_transaction: TransactionTable = (
            user_services.get_transaction_by_date_desc_bank(
                db=db,
                bank=bank,
                date=new_transaction.date,
                desc=new_transaction.description,
            )
        )

        if db_transaction is not None:
            fprint("The transaction already exists in the database.")
            return

        bank_ins: BANK_INSTANCE_TYPE = BANK_INST[bank]

        trans_table_list: list[TransactionTable] = []

        # check if the transaction can be classify automatically
        if is_transaction_auto_classifiable(
            database_url=database_url,
            product=product,
            trans_desc=new_transaction.description,
            bank=bank,
        ):
            if typer.confirm(
                "This transaction can be classified automatically. Do you want to classify it?"
            ):
                transaction: CreateTransactionBM | None = classify_transaction_auto(
                    transaction=new_transaction,
                    bank=bank,
                    institution=bank_ins,
                    database_url=database_url,
                    financial_product=product,
                )

                # save transaction in the database
                if transaction is not None:

                    trans_table_list.append(
                        TransactionTable(**transaction.model_dump())
                    )

                    user_services.create_transaction(
                        db=db,
                        transactions=trans_table_list,
                    )

                    fprint("The transaction was added successfully.")
                    return

                else:
                    fprint_panel(
                        msg="An error occurred during classification. We will classify the transaction manually.",
                        title="Auto Classification Fail",
                    )

        # Display account name
        account: AccountSectionEnum = typer.prompt(
            type=AccountSectionEnum,
            text=f"Please select an account ({[section.value for section in AccountSectionEnum]})",
        )

        db_account: AccountTable = user_services.get_account_id_by_name(
            db=db, account_name=account.value
        )

        if db_account is None:
            fprint_panel(
                msg="No specified account name was found in the database.",
                title="Account name error",
                color="red",
            )
            raise typer.Abort()

        # Display subcategory
        db_subcat: Sequence[SubCategoryTable] = user_services.get_all_subcategory(db)

        if len(db_subcat) == 0:
            fprint(
                "Please create one or more subcategories before using the [green]"
                "create transaction"
                "[/green] command."
            )
            raise typer.Abort()

        subcat_dict, subcat_choice = build_choice(db_subcat, "categogy")

        subcat_id: int = prompt_choice(
            subcat_choice,
            "Select the subcategory",
            new_transaction.description,
        )

        # Display classification

        db_class: Sequence[ClassificationTable] = user_services.get_all_classification(
            db=db,
        )

        class_dict, class_choice = build_choice(db_class)

        cls_id: int = prompt_choice(
            class_choice,
            "Select the classification",
            new_transaction.description,
        )

        new_transaction.account_id = db_account.id
        new_transaction.subcategory_id = subcat_id
        new_transaction.classification_id = cls_id

        # Add transaction to the database
        trans_table_list.append(TransactionTable(**new_transaction.model_dump()))
        user_services.create_transaction(db=db, transactions=trans_table_list)

    fprint("The transaction was added successfully.")


@app.command(help="Allows you to add a new classification.")
def classification(
    name: Annotated[
        str,
        typer.Option(
            "--name",
            "-n",
            help="Classification name",
            prompt="Please enter the name of the classification",
        ),
    ],
):
    # Get the user database URL
    database_url: str = auth.get_user_database_url()

    with get_db(db_path=database_url, db_type=DatabaseType.USER) as db:

        # Check if the new classification exists in the database
        db_class: ClassificationTable | None = user_services.get_classification_by_name(
            db, name
        )

        if db_class is not None:
            fprint("This classification already exists.")
            raise typer.Abort()

        # Add the new classification to the database
        new_class: ClassifySchemas = ClassifySchemas(
            name=name,
        )

        user_services.create_new_classification(db, [new_class])

    fprint("The classification has been added successfully.")


@app.command(help="Allows you to create bank accounts")
def bank_account(
    account_type: Annotated[
        AccountTypeEnum,
        typer.Option(
            "--account_type",
            "-a",
            help="Type of bank account",
            prompt="What is the type of bank account?",
        ),
    ] = None,
    name: Annotated[
        str,
        typer.Option(
            "--name",
            "-n",
            help="Name or nickname of the bank account",
            prompt="what is the name or nickname of the bank account?",
        ),
    ] = None,
    amount: Annotated[
        float,
        typer.Option(
            "--amount",
            help="Amount in your bank account as of today",
            prompt="How much is in your bank account as of today?",
        ),
    ] = None,
):

    # Retrieve the user's database URL
    database_url: str = auth.get_user_database_url()

    try:

        with get_db(db_path=database_url, db_type=DatabaseType.USER) as db:

            # Fetch banking institution data to select the bank name
            db_institution: Sequence[BankingInstitutionTable] = (
                service.banking_institution.get_all_bank_institution(db)
            )

            # Check if the database returns an empty list
            if is_empty_list(db_institution) == False:
                color: str = "green"
                fprint(
                    f"Please define an institution with the [{color}]add institution[/{color}] command."
                )
                raise typer.Abort()

            # Display options for banking institutions
            dict_institution, choice_institution = build_choice(db_institution)

            institution_id: int = prompt_choice(
                choice_institution, "Select a institution", ""
            )

            # Add the bank account to the database
            service.bank_account.create_new_bank_Account(
                account_type=account_type.value,
                amount=amount,
                bank_id=institution_id,
                db=db,
                name=name,
            )

            fprint("The bank account was added successfully")

    except Exception as e:
        fprint(e)
