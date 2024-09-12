import pandas as pd
from pandas import DataFrame
from rich.table import Table


def group_transaction(df: DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    grouped_subcategory: DataFrame = (
        df.groupby(["category_name", "subcategory_name"])
        .agg({"amount": "sum"})
        .reset_index()
    )
    grouped_subcategory["amount"] = grouped_subcategory["amount"].round(2)

    grouped_category: DataFrame = (
        grouped_subcategory.groupby("category_name")
        .agg({"amount": "sum"})
        .reset_index()
    )
    grouped_category["amount"] = grouped_category["amount"].round(2)

    return grouped_category, grouped_subcategory


def add_category(table: Table, category_name: str, amount: float) -> None:
    table.add_row(f" {category_name}", f"{str(amount)} $")


def add_subcategory(table: Table, sub_grouped: DataFrame) -> None:
    for _, subcategory_row in sub_grouped.iterrows():
        sub_name: str = subcategory_row["subcategory_name"]
        sub_amount: float = subcategory_row["amount"]

        table.add_row(f"{" "*4}{sub_name}", f"{sub_amount} $")
