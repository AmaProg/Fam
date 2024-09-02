from typing import Any, Sequence
import pandas as pd
from pandas import DataFrame
from rich.table import Table
from rich.console import Console

from fam.database.users.models import TransactionTable
from fam.database.users.schemas import TransactionBaseModel


def generate_invoice_table(
    transaction_list: Sequence[TransactionTable],
    classification_name: str,
    invoice_title: str,
) -> None:
    # Initialisation du tableau Rich avec un titre
    table: Table = Table(title=invoice_title)
    headers: list[str] = []

    # Conversion des transactions en une liste de dictionnaires
    transaction_model_list: list[dict[str, Any]] = [
        TransactionBaseModel(
            class_name=classification_name,
            category_name=t.subcategory.category.name,
            subcategory_name=t.subcategory.name,
            amount=t.amount,
            pay_ratio=int(t.payment_proportion * 100),
        ).model_dump()
        for t in transaction_list
    ]

    # Conversion de la liste en DataFrame pandas
    df: DataFrame = pd.DataFrame(data=transaction_model_list)

    # Ajout des colonnes au tableau
    headers.extend(
        [
            classification_name.capitalize(),
            "Category",
            "Subcategory",
            "Amount [$]",
            "Pay Ratio [%]",
            "Adjusted Amount [$]",
        ]
    )

    for header in headers:
        table.add_column(header=header, justify="left")

    # Grouper les données par catégorie et sous-catégorie
    grouped_subcategory = (
        df.groupby(["category_name", "subcategory_name"])
        .agg(
            {
                "amount": "sum",
                "pay_ratio": "first",
            }  # Utiliser 'first' pour prendre la première valeur de pay_ratio
        )
        .reset_index()
    )

    # Grouper par catégorie pour obtenir les totaux
    grouped_category = (
        grouped_subcategory.groupby("category_name")
        .agg({"amount": "sum"})
        .reset_index()
    )

    current_category = None

    total_amount = 0.0  # Initialisation pour le total global
    total_adjusted_amount = 0.0  # Initialisation pour le montant ajusté global

    # Boucle pour ajouter les lignes au tableau
    for _, category_row in grouped_category.iterrows():
        category = category_row["category_name"]
        category_total_amount = category_row["amount"]
        category_adjusted_amount = (
            grouped_subcategory[grouped_subcategory["category_name"] == category]
            .apply(lambda row: row["amount"] * (row["pay_ratio"] / 100), axis=1)
            .sum()
        )

        total_amount += category_total_amount  # Ajouter au total global
        total_adjusted_amount += (
            category_adjusted_amount  # Ajouter au montant ajusté global
        )

        if current_category != category:
            if current_category is not None:
                # Ligne vide pour séparer les catégories
                table.add_row(*[""] * len(headers), "")

            # Ligne pour la catégorie
            table.add_row(
                classification_name,
                category,
                "",
                "",
                "",
                f"{category_adjusted_amount:.2f}",
            )

            current_category = category

        # Ajouter les sous-catégories
        subcategory_group = grouped_subcategory[
            grouped_subcategory["category_name"] == category
        ]
        for _, subcategory_row in subcategory_group.iterrows():
            subcategory = subcategory_row["subcategory_name"]
            amount = subcategory_row["amount"]
            pay_ratio = subcategory_row["pay_ratio"]
            adjusted_amount = amount * (pay_ratio / 100)  # Calculer le montant ajusté

            table.add_row(
                "",
                "",
                subcategory,
                f"{amount:.2f}",
                f"{pay_ratio}%",
                f"{adjusted_amount:.2f}",
            )

    # Ligne de total global
    table.add_row("", "", "Total Global", "", "", f"{total_adjusted_amount:.2f}")

    # Affichage du tableau dans la console
    console: Console = Console()
    console.print(table)
    print("")
