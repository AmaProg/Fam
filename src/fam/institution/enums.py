from enum import Enum


class AccountTypeEnum(str, Enum):
    SAVE_ACCOUNT = "save account"
    CHECK_ACCOUNT = "check account"
    CREDIT_CARD_ACCOUNT = "credit_card_account"
