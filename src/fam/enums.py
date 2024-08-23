from enum import Enum


class BankEnum(str, Enum):
    BMO = "bmo"
    TANGERINE = "tangerine"


class FinancialProductEnum(Enum):
    CREDIT_CARD = "credit card"
    CHECKING_ACCOUNT = "check account"


class AccountSection(Enum):
    INCOME = "income"
    EXPENSE = "expense"
    ASSET = "asset"
    PASSIVE = "passive"
