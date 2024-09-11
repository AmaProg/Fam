from enum import Enum


class BankEnum(str, Enum):
    BMO = "bmo"
    TANGERINE = "tangerine"


class InstitutionEnum(Enum):
    BMO = "BMO"
    TD = "TD"
    RBC = "RBC"
    SCOTIA = "Scotiabank"
    CIBC = "CIBC"
    NATIONAL = "National"
    HSBC = "HSBC"
    DESJARDINS = "Desjardins"
    WEALTHSIMPLE = "Wealthsimple"
    QUESTRADE = "Questrade"
    PC = "PC Financial"
    EQ = "EQ Bank"
    MANULIFE = "Manulife"
    TANGERINE = "Tangerine"


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


class FinancialAccountEnum(Enum):
    SAVINGS_ACCOUNT = "Épargne"
    CPG = "CPG"
    CELI = "CELI"
    CELIAPP = "CELIAPP"
    REER = "REER"
    REEE = "REEE"
    BROKERAGE_ACCOUNT = "Compte de Courtage"
    STOCK = "bourse"
    REAL_ESTATE = "Immobilier"
    PRECIOUS_METALS = "Métaux Précieux"
    CD = "Certificat de Dépôt"
    ESP = "Épargne-Salaire"
