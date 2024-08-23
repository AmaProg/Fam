from copy import copy
from tkinter import filedialog
from typing import Any
from pandas import DataFrame
from pandas import DataFrame
from sqlalchemy.orm import Session
import typer
import pandas as pd

from fam.command.utils import  date_to_timestamp_by_bank, show_choice
from fam.database.users.models import (
    T,
    SubCategoryTable,
    TransactionTable,
)
from fam.database.users.schemas import CreateTransactionBM
from fam.enums import BankEnum, FinancialProductEnum
from fam.bank.bmo import bmo
from fam.database.users import services as user_services


def open_dialog_file(bank: str) -> str:
    csv_filename: str = filedialog.askopenfilename(
        title=f"select the statement for the {bank} bank",
        filetypes=(("CSV files", "*.csv"),),
    )

    return csv_filename


def read_csv_by_bank(filename: str, bank: BankEnum) -> DataFrame | None:

    func: dict[BankEnum, Any] = {
        BankEnum.BMO: pd.read_csv(filename, skiprows=1),
        BankEnum.TANGERINE: pd.read_csv(filename),
    }

    df = func.get(bank, None)

    return df


def classify_transactions(df: DataFrame, subcat_choice: list[str], class_choice: list[str], subcat_dict: dict[int, SubCategoryTable], product: FinancialProductEnum, bank: BankEnum, db: Session) -> list[TransactionTable]:
    # Classify all transaction
    transactions: list[TransactionTable] = []

    for idx, transaction in df.iterrows():
        
        # promp question for each transaction
        
        show_choice(subcat_choice)
        subcat_id: int = typer.prompt(type=int, text=f"Select a category for {transaction["Description"]}")
        
        if subcat_id == 0:
            continue
        
        show_choice(class_choice)
        cls_id: int = typer.prompt(type=int, text=f"Select a class for {transaction["Description"]}")
        
        sub_table: SubCategoryTable = subcat_dict.get(subcat_id, None)
        
        if sub_table is None:
            raise typer.Abort
        
        new_transaction: CreateTransactionBM = CreateTransactionBM(
            description=transaction[bmo.csv_header.description],
            product=product.value,
            amount=transaction[bmo.csv_header.transaction_amount],
            date=date_to_timestamp_by_bank(str(transaction[bmo.csv_header.transaction_date]), bank),
            bank_name=bank.value,
            classification_id=cls_id,
            subcategory_id=subcat_id,
            account_id=sub_table.category.account.id
        )
        
        trans_table: TransactionTable | None =  user_services.get_transaction_by_date_desc_bank(
            db=db,
            date=new_transaction.date,
            desc=new_transaction.description,
            bank=bank,
        )
        
        if trans_table is not None:
            if typer.confirm(text=f"The following description {new_transaction.description} already exists. Do you want to replace it?"):
                user_services.update_transaction_by_desc(db, new_transaction.description, new_transaction)
                continue
            else:
                continue
                
        
        
        transactions.append(TransactionTable(**copy.copy(new_transaction.model_dump())))
        
    return transactions
