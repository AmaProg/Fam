from enum import Enum


class BankEnum(str, Enum):
    BMO = "bmo"
    TANGERINE = "tangerine"


class FinancialProductEnum(Enum):
    CREDIT_CARD = "credit card"
    CHECKING_ACCOUNT = "check account"


class AccountSectionEnum(Enum):
    INCOME = "income"
    EXPENSE = "expense"
    ASSET = "asset"
    PASSIVE = "passive"


class TransactionTypeEnum(Enum):
    CREDIT = "credit"
    DEBIT = "debit"


class InvoiceTypeEnum(Enum):
    CREDIT_CARD = "credit card"


class AccountTypeEnum(Enum):
    CHECK_ACCOUNT = "check"
    INVESTMENT_ACCOUNT = "investment"
    SAVE_ACCOUNT = "save"
