from fam.bank import constants as kbank
from fam.enums import FinancialProductEnum
from fam.security import generate_transaction_hash


def extract_transaction_details(
    transaction: dict,
    institution: kbank.BANK_INSTANCE_TYPE,
    financial_product: FinancialProductEnum,
) -> tuple[str, float, str, str]:
    """
    Extrait les détails de la transaction en utilisant les méthodes de l'institution financière.

    :param transaction: Dictionnaire représentant une transaction.
    :param institution: Instance de la classe FinancialInstitution.
    :param financial_product: Nom du produit financier.
    :return: Un tuple contenant la description, le montant de la transaction et la date de la transaction et le hash.
    """
    desc_head: str = institution.get_description(financial_product)
    amount_head: str = institution.get_transaction_amount(financial_product)
    date_head: str = institution.get_transaction_date(financial_product)

    description: str = transaction[desc_head]
    transaction_amount: float = transaction[amount_head]
    transaction_date: str = transaction[date_head]

    transaction_hash: str = generate_transaction_hash(transaction)

    return description, transaction_amount, transaction_date, transaction_hash
