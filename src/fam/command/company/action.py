from typing import Dict, List
import pandas as pd
import typer
import yaml
from pandas import DataFrame
from enums.bank import BankEnum


# Charger les catégories depuis un fichier YAML
def load_categories(file_path: str) -> Dict[str, List[str]]:
    with open(file_path, "r") as file:
        return yaml.safe_load(file)


# Sauvegarder les catégories dans un fichier YAML
def save_categories(file_path: str, categories: Dict[str, List[str]]) -> None:
    with open(file_path, "w") as file:
        yaml.dump(categories, file, default_flow_style=False)


# Charger les catégories depuis le fichier YAML
categories = load_categories("categories.yaml")


def display_categories():
    # Affiche les catégories existantes avec des numéros
    typer.echo("Available categories:")
    for idx, category in enumerate(categories.keys(), start=1):
        typer.echo(f"{idx}. {category}")


def assign_category(description: str) -> str:
    # Cherche la catégorie existante
    for category, keywords in categories.items():
        if isinstance(keywords, list) and any(
            keyword in description for keyword in keywords
        ):
            return category

    # Si la catégorie n'est pas trouvée, demander à l'utilisateur de choisir une catégorie existante ou en créer une nouvelle
    typer.echo(f"\nDescription not categorized: '{description}'")
    display_categories()

    # Demander à l'utilisateur de choisir une catégorie ou d'en créer une nouvelle
    choice = typer.prompt("Choose an existing category by number or type a new one:")

    # Vérifier si la saisie est un nombre entier
    try:
        choice = int(choice)
        if 1 <= choice <= len(categories):
            new_category = list(categories.keys())[choice - 1]
        else:
            raise ValueError
    except ValueError:
        new_category = (
            choice  # Utiliser la saisie de l'utilisateur comme nouvelle catégorie
        )
        if new_category not in categories:
            categories[new_category] = (
                []
            )  # Initialiser une liste vide pour la nouvelle catégorie

    # Ajouter la description dans la catégorie spécifiée
    if description not in categories[new_category]:
        categories[new_category].append(description)

    save_categories("categories.yaml", categories)

    return new_category


def create_new_expense_category(bank: BankEnum, statement: DataFrame):

    if bank == BankEnum.BMO:

        for idx, row in statement.iterrows():

            amount: float = row["Montant de la transaction"]

            if amount <= -1:
                statement.drop(idx, inplace=True)

        statement.reset_index(drop=True, inplace=True)

        statement.index = statement.index + 1

        df_expense: DataFrame = pd.DataFrame(columns=["name", "category"])

        df_expense["name"] = statement["Description"]

        # Assigner les catégories en utilisant la fonction assign_category
        df_expense["category"] = df_expense["name"].apply(assign_category)

        print(df_expense)

    elif bank == BankEnum.TANGERINE:
        pass

    else:
        pass
