from copy import copy
from typing import Any, Sequence

import typer
from fam.command.bank import account
from fam.database.users.models import AccountTable, CategoryTable, ClassificationTable
from fam.database.users.schemas import (
    AccountSchemas,
    CategorySchemas,
    ClassifySchemas,
    CreateSubCategory,
)
from fam.database.users import service
from sqlalchemy.orm import Session

from fam.enums import AccountSectionEnum, AccountTypeEnum
from fam.utils import fprint


def init_account_table(db: Session) -> Sequence[AccountTable]:
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

        account_schemas_list.append(account_schemas)

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


def init_category_table(
    db: Session,
    accounts: Sequence[AccountTable],
) -> None:

    category_data: dict[str, Any] = {
        "income": {
            "id": "",
            "name": category_name_for_income_account(),
            "description": category_desc_for_income_Account(),
            "subcategories": subcategory_for_income_account(),
        },
        "expense": {
            "id": "",
            "name": category_name_for_expense_account(),
            "description": categeory_desc_for_expense_account(),
            "subcategories": subcategory_for_expense_account(),
        },
        "asset": {
            "id": "",
            "name": category_name_for_asset_account(),
            "description": category_desc_for_asset_account(),
            "subcategories": subcategory_for_asset_account(),
        },
        "passive": {
            "id": "",
            "name": category_name_for_passive_account(),
            "description": category_desc_for_passive_account(),
            "subcategories": subcategory_for_passive_account(),
        },
    }

    account_mapping = {
        AccountSectionEnum.INCOME.value: "income",
        AccountSectionEnum.EXPENSE.value: "expense",
        AccountSectionEnum.ASSET.value: "asset",
        AccountSectionEnum.PASSIVE.value: "passive",
    }

    for account in accounts:
        category_key = account_mapping.get(account.name)

        if category_key:
            category_data[category_key]["id"] = account.id
        else:
            fprint("Fail to create category")
            raise typer.Abort()

    for key in category_data.keys():

        id: int = category_data[key]["id"]
        names: list[str] = category_data[key]["name"]
        desc: list[str] = category_data[key]["description"]
        subcat: list[list[str]] = category_data[key]["subcategories"]

        build_category_table(
            names=names,
            desc=desc,
            account_id=id,
            db=db,
            subcats=subcat,
        )


def build_category_table(
    names: list[str],
    desc: list[str],
    account_id: int,
    subcats: list[list[str]],
    db: Session,
) -> None:

    for idx, name in enumerate(names):

        try:

            category_schemas: CategorySchemas = CategorySchemas(
                name=name,
                description=desc[idx],
                account_id=account_id,
            )

            db_category: CategoryTable = service.category.create_new_category(
                db,
                category_schemas,
            )

            build_subcategory(
                subcategories=subcats[idx],
                category_id=db_category.id,
                db=db,
            )

        except Exception as e:
            fprint(e)


def build_subcategory(subcategories: list[str], category_id: int, db: Session) -> None:

    for name in subcategories:

        subcategory_schemas: CreateSubCategory = CreateSubCategory(
            name=name,
            category_id=category_id,
        )

        service.subcategory.create_subcategory(db, subcategory_schemas)


def category_name_for_income_account() -> list[str]:
    return [
        "Placements",
        "Revenu",
    ]


def category_name_for_asset_account() -> list[str]:
    return [
        "Actif a court terme",
        "Actif a long terme",
    ]


def category_name_for_passive_account() -> list[str]:
    return [
        "Passif a court terme",
        "Passif a long terme",
    ]


def category_name_for_expense_account() -> list[str]:
    return [
        "Habitation",
        "Assurance Personnelles",
        "Transport",
        "Telecommunications",
        "Alimentation",
        "Sante",
        "Loisirs et education",
        "Remboursement d'emprunts",
        "Les enfants",
        "Soins Personnels",
        "Epargne",
        "Autres",
        "Frais Financier",
        "Charges Fiscales",
        "Services Financiers",
        "Frais Bancaires",
        "Opérations Internes",
    ]


def category_desc_for_income_Account() -> list[str]:
    return [
        "Revenu généré par les investissements, y compris les intérêts, dividendes, et autres gains de placement",
        "Toutes les sources de revenu, incluant le salaire, les remboursements, et autres entrées d'argent",
    ]


def category_desc_for_asset_account() -> list[str]:
    return [
        "Actifs qui peuvent être convertis en liquidités rapidement, généralement en moins d'un an. Cela inclut les liquidités, les comptes d'épargne, et les investissements facilement vendables.",
        "Actifs qui ne peuvent pas être convertis en liquidités rapidement, souvent sur une période supérieure à un an. Cela inclut les immobilisations, les biens immobiliers, et les investissements à long terme.",
    ]


def category_desc_for_passive_account() -> list[str]:
    return [
        "Passifs devant être réglés dans un délai court, généralement en moins d'un an, tels que les dettes à court terme et les créances fournisseurs.",
        "Passifs qui ne sont pas exigibles immédiatement, souvent sur une période supérieure à un an, comme les emprunts à long terme et les obligations.",
    ]


def categeory_desc_for_expense_account() -> list[str]:
    return [
        "Depense liee au logement",
        "Depense liee aux assurances",
        "Depense liee au transport",
        "Depense liee a la telecommunication",
        "Depense liee a l'alimentation",
        "Depense liee a la sante personnelle",
        "Depense liee a l'education et aux loisirs",
        "Depense liee au remboursement des dettes",
        "Depense liee aux enfants",
        "Depense liee aux soins personnels",
        "Depense liee a l'epargne",
        "Autres depenses qui ne peuvent pas etre classees",
        "Depense liee aux frais financiers dus aux placements",
        "Dépenses liées aux impôts sur les gains en capital et autres obligations fiscales.",
        "Dépenses liees aux services financiers, y compris les frais de comptable, de conseiller financier, et autres services professionnels.",
        "Dépenses liées aux frais bancaires, tels que les frais de tenue de compte, les frais de transaction et les frais de découvert.",
        "Gestion des opérations internes et des transferts entre comptes",
    ]


def subcategory_for_income_account() -> list[list[str]]:
    return [
        ["Revenus d'Interets", "Dividendes"],
        [
            "Salaire net",
            "Remboursement d'impot",
            "Autres revenu",
            "Remboursement de pret",
            "Remise en argent",
        ],
    ]


def subcategory_for_asset_account() -> list[list[str]]:
    return [
        ["Tresorerie", "Compte Bancaire"],
        ["Immobilisation financière"],
    ]


def subcategory_for_passive_account() -> list[list[str]]:
    return [
        ["Capitaux propre"],
        ["Carte de credit", "Pret Etudiant", "Marge de credit"],
    ]


def subcategory_for_expense_account() -> list[list[str]]:
    return [
        ["Loyer", "Electricite", "Assurance Habitation"],
        ["Assurance vie", "Assurance medicament"],
        [
            "Essence",
            "Entretiens et Reparation",
            "Abonnement Routier",
            "Permis de conduire",
            "Constat d'infraction",
        ],
        ["Cellulaire", "Internet"],
        ["Epicerie", "Restaurant"],
        ["Medicament", "Dentaire"],
        ["Abonnement", "Vacances"],
        [
            "Carte de credit CAD",
            "Marge de credit",
            "Pret etudiant",
            "Carte de credit USD",
            "Interet",
            "Frais Annuel",
        ],
        ["Frais de garde", "Autres depenses"],
        ["Cheveux", "Vetement"],
        ["Fond d'urgence", "Liberte financier"],
        ["Startup", "OIQ", "Depense divers"],
        ["Frais de placement", "Frais de courtage", "Pertes sur créances"],
        ["Impôt sur interet"],
        ["Comptable"],
        ["Frais de Service Bancaire", "Frais de Transaction", "Frais de Découvert"],
        ["Transfert entre comptes internes"],
    ]
