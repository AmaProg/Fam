from copy import copy
from os import name
from typing import Any
from webbrowser import get
from pandas import DataFrame
from sqlalchemy import ScalarResult
import typer

from fam.command.adding import utils
from fam.database.users.models import CategoryTable, ClassificationTable, TransactionTable
from fam.database.users.schemas import CreateTransactionBM
from fam.enums import BankEnum
from fam.utils import fprint


def classify_transaction(
    df: DataFrame,
    bank_name: BankEnum,
    categories: ScalarResult[CategoryTable],
    class_transaction: ScalarResult[ClassificationTable]
) -> list[TransactionTable]:

    func: dict[str, Any] = {
        BankEnum.BMO: utils.classify_bmo_transactions,
        BankEnum.TANGERINE: utils.classify_tangerine_transactions,
    }
    

    transactions: list[TransactionTable] = []
    cat_choice: list[str] = []
    class_choice: list[str] = []
    cat_dict: dict[int, CategoryTable] = {}
    class_dict: dict[int, ClassificationTable] = {}
    
    for category in categories:
        cat_dict[category.id] = copy(category)
        cat_choice.append(copy(f"{category.id}: {category.name}"))
        
    for classify in class_transaction:
        class_dict[classify.id] = copy(classify)
        class_choice.append(copy(f"{classify.id}: {classify.name}"))
        

    for idx, transaction in df.iterrows():

        # promp question for each transaction
        cat_id: int = typer.prompt(type=int, text=f"{cat_choice}\n\nSelect a category for {transaction["Description"]}",)
        cls_id: int = typer.prompt(type=int, text=f"{class_choice}\n\nSelect a class for {transaction["Description"]}",)
        
        category_data: CategoryTable | None = cat_dict.get(cat_id, None)
        class_data: ClassificationTable | None = class_dict.get(cls_id, None)
        
        if category_data is None:
            fprint(f"Category {transaction["Description"]} cannot be categorized.")
            continue
        
        if class_data is None:
            fprint(f"Category {transaction["Description"]} cannot be categorized.")
            continue
        
        desc = transaction["Description"]
        amount = transaction["Montant de la transaction"]
        date = int(transaction["Date de la transaction"])
        
        new_transaction: CreateTransactionBM = CreateTransactionBM(
            description= desc,
            amount= amount,
            date=date,
            account_id=category_data.account_id,
            category_id=category_data.id,
            classification_id=class_data.id,
            
        )
        
        transactions.append(TransactionTable(**copy(new_transaction.model_dump())))
        
        break
        
        
    return transactions
        
        
