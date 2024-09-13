from enum import Enum

tangerine: str = "tangerine".lower()
bmo: str = "bmo"
credit_card: str = "credit card"
check_account: str = "check account"
save_account: str = "save account"


class BankEnum(str, Enum):
    BMO = bmo
    TANGERINE = tangerine


class InstitutionEnum(Enum):
    BMO = bmo
    TD = "TD".lower()
    RBC = "RBC".lower()
    SCOTIA = "Scotiabank".lower()
    CIBC = "CIBC".lower()
    NATIONAL = "National".lower()
    HSBC = "HSBC".lower()
    DESJARDINS = "Desjardins".lower()
    WEALTHSIMPLE = "Wealthsimple".lower()
    QUESTRADE = "Questrade".lower()
    PC = "PC Financial".lower()
    EQ = "EQ Bank".lower()
    MANULIFE = "Manulife".lower()
    TANGERINE = tangerine


class FinancialProductEnum(Enum):
    CREDIT_CARD = credit_card
    CHECKING_ACCOUNT = check_account
    SAVE_ACCOUNT = save_account


class AccountSectionEnum(Enum):
    INCOME = "income"
    EXPENSE = "expense"
    ASSET = "asset"
    PASSIVE = "passive"


class TransactionTypeEnum(Enum):
    CREDIT = "credit"
    DEBIT = "debit"


class InvoiceTypeEnum(Enum):
    CREDIT_CARD = credit_card


class AccountTypeEnum(Enum):
    CHECK_ACCOUNT = check_account
    INVESTMENT_ACCOUNT = "investment"
    SAVE_ACCOUNT = save_account


class FinancialAccountEnum(Enum):
    CHECK_ACCOUNT = check_account
    SAVINGS_ACCOUNT = save_account
    CPG = "CPG".lower()
    CELI = "CELI".lower()
    CELIAPP = "CELIAPP".lower()
    REER = "REER".lower()
    REEE = "REEE".lower()
    BROKERAGE_ACCOUNT = "BROKERAGE_ACCOUNT".lower()
    STOCK = "STOCK".lower()
    REAL_ESTATE = "REAL_ESTATE".lower()
    PRECIOUS_METALS = "PRECIOUS_METALS".lower()
    CD = "Certificate of Deposit".lower()
