from fam.bank import bmo, tangerine
from fam.enums import BankEnum


BANK_INST = {
    BankEnum.BMO: bmo.BMO(),
    BankEnum.TANGERINE: tangerine.Tangerine(),
}

BANK_INSTANCE_TYPE = bmo.BMO | tangerine.Tangerine
