from fam.bank import BMO, Tangerine, Desjardin
from fam.enums import BankEnum


BANK_INST = {
    BankEnum.BMO: BMO(),
    BankEnum.TANGERINE: Tangerine(),
    BankEnum.DESJARDIN: Desjardin(),
}

BANK_INSTANCE_TYPE = BMO | Tangerine | Desjardin
