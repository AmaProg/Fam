import copy
from pathlib import Path
from typing import Any
from typing_extensions import Annotated
from pandas import DataFrame
from sqlalchemy import ScalarResult
from typer import Typer
from tkinter import filedialog
import typer
import pandas as pd

from fam import auth
from fam.command.adding import action
from fam.database.db import DatabaseType, get_db
from fam.database.users.models import (
    CategoryTable,
    ClassificationTable,
    TransactionTable,
)
from fam.database.users.schemas import CreateTransactionBM
from fam.enums import BankEnum, FinancialProductEnum
from fam.utils import fprint
from fam.database.users import services as user_services

app = Typer(help="Allows you to add items to the folder.")

add_command: dict[str, Any] = {"app": app, "name": "add"}


@app.command()
def statement(
    filename: Annotated[str, typer.Option("--filename", "-f", help="")] = None,
    product: Annotated[
        FinancialProductEnum, typer.Option("--product", "-p", help="")
    ] = None,
):

    # Get user session.
    session = auth.get_user_session()

    database_url: str = session["database_url"]

    # Ask the user for which financial product the statement is
    if product is None:
        product_name: FinancialProductEnum = typer.prompt(
            type=FinancialProductEnum,
            text=f"What is the financial product {[choice.name.lower() for choice in FinancialProductEnum]}? ",
            show_choices=True,
        )

    # Ask the user which bank the statement comes from.
    bank_name: BankEnum = typer.prompt(
        type=BankEnum,
        text=f"which bank does the bank statement come from {[choice.name.lower() for choice in BankEnum]}? ",
        show_choices=False,
    )

    # Get csv file and convert to dataframe
    if filename is None:
        # open dialogFile
        csv_filename: str = filedialog.askopenfilename(
            title=f"select the statement for the {bank_name.name} bank",
            filetypes=(("CSV files", "*.csv"),),
        )
        if csv_filename == "":
            raise typer.Abort()
    else:
        csv_filename = filename

    if Path(csv_filename).suffix.lower() != ".csv":
        fprint("Invalid file format: not a CSV.")
        raise typer.Abort()

    df_csv: DataFrame = pd.read_csv(csv_filename, skiprows=1)

    with get_db(db_path=database_url, db_type=DatabaseType.USER) as db:

        # Get all category
        categories: ScalarResult[CategoryTable] = user_services.get_all_category(db)
        classifies: ScalarResult[ClassificationTable] = (
            user_services.get_all_classification(db)
        )

        # By category build category and classification choice
        cat_dict: dict[int, CategoryTable] = {}
        cat_choice: list[str] = []
        
        for category in categories:
            cat_dict.update({category.id: category})
            cat_choice.append(copy.copy(f"{category.id}: {category.name} ({category.account.name})"))
        
    
        class_dict: dict[int, ClassificationTable] = {}
        class_choice: list[str] = []
        
        for classify in classifies:
            class_dict.update({classify.id: classify})
            class_choice.append(f"{classify.id} : {classify.name}")

        # Classify all transaction
        transactions: list[TransactionTable] = []

        for idx, transaction in df_csv.iterrows():
            # promp question for each transaction
            print("\n".join(cat_choice))
            cat_id: int = typer.prompt(type=int, text=f"Select a category for {transaction["Description"]}",show_choices=True, show_default=True,)
            print("\n".join(class_choice))
            cls_id: int = typer.prompt(type=int, text=f"Select a class for {transaction["Description"]}",show_choices=True, show_default=True,)
            
            cat_table: CategoryTable = cat_dict.get(cat_id, None)
            
            new_transaction: CreateTransactionBM = CreateTransactionBM(
                description=transaction["Description"],
                amount=transaction["Montant de la transaction"],
                date=transaction["Date de la transaction"],
                classification_id=cls_id,
                category_id=cat_id,
                account_id=cat_table.account.id
            )
            
            
            
            transactions.append(TransactionTable(**copy.copy(new_transaction.model_dump())))

        # Save all transactions that have been categorized in the database
        user_services.create_transaction(db, transactions)

    # print success transaction
    fprint("Assignment of categories to the transaction was successfully completed.")

    # # Get de user session
    # session = auth.get_user_session()

    # database_url: str = session["database_url"]

    # # Ask the user which bank the statement comes from.
    # bank_name: BankEnum = typer.prompt(
    #     type=BankEnum,
    #     text=f"which bank does the bank statement come from {[choice.name.lower() for choice in BankEnum]}? ",
    #     show_choices=False,
    # )

    # if filename == None:

    #     # open dialogFile
    #     csv_filename: str = filedialog.askopenfilename(
    #         title=f"select the statement for the {bank_name.name} bank",
    #         filetypes=(("CSV files", "*.csv"),),
    #     )

    #     if csv_filename == "":
    #         raise typer.Abort()
    # else:
    #     csv_filename = filename

    # # check if it is cs file.
    # if Path(csv_filename).suffix.lower() != ".csv":
    #     fprint("Invalid file format: not a CSV.")
    #     raise typer.Abort()

    # df_csv: DataFrame = pd.read_csv(csv_filename, skiprows=1)

    # # assingn category for all transaction
    # with get_db(db_path=database_url, db_type=DatabaseType.USER) as db:

    #     # Get categories list
    #     cat_list: ScalarResult[CategoryTable] = user_services.get_all_category(db)
    #     classify: ScalarResult[ClassificationTable] = (
    #         user_services.get_all_classification(db)
    #     )

    #     transactions: list[TransactionTable] = action.classify_transaction(
    #         df=df_csv,
    #         bank_name=bank_name,
    #         categories=cat_list,
    #         class_transaction=classify,
    #     )

    #     # save de assignation on the database
    #     user_services.create_transaction(db, transactions)

    pass
