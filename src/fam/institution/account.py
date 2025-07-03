from dataclasses import dataclass


@dataclass
class CreditCard:
    article_number: str = ""
    carte_number: str = ""
    date_registering_statement: str = ""
    description: str = ""
    amount: str = ""
    transaction_date: str = ""
    sign_reversed: bool = False


@dataclass
class CheckAccount:
    header_amount: str = ""
    header_description: str = ""
    header_maxi_card: str = ""
    header_registration_date: str = ""
    header_transaction_type: str = ""
    header_name: str = ""
    sign_reversed: bool = False


@dataclass
class SaveAccount:
    amount: str = ""
    description: str = ""
    maxi_card: str = ""
    registration_date: str = ""
    transaction_type: str = ""
    name: str = ""
    sign_reversed: bool = False
