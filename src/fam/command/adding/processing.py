from fam.bank import constants as kbank
from fam.enums import FinancialProductEnum


def extract_transaction_details(
    transaction: dict,
    institution: kbank.BANK_INSTANCE_TYPE,
    financial_product: FinancialProductEnum,
) -> tuple[str, float, str]:
    """
    Extrait les détails de la transaction en utilisant les méthodes de l'institution financière.

    :param transaction: Dictionnaire représentant une transaction.
    :param institution: Instance de la classe FinancialInstitution.
    :param financial_product: Nom du produit financier.
    :return: Un tuple contenant la description, le montant de la transaction et la date de la transaction.
    """
    description: str = transaction[institution.get_description(financial_product)]
    transaction_amount: float = transaction[
        institution.get_transaction_amount(financial_product)
    ]
    transaction_date: str = transaction[
        institution.get_transaction_date(financial_product)
    ]

    return description, transaction_amount, transaction_date
