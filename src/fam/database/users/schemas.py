from pydantic import BaseModel


class AccountSchemas(BaseModel):
    name: str
    description: str


class CategoryBM(BaseModel):
    name: str
    description: str
    account_id: int


class CreateTransactionBM(BaseModel):
    description: str
    product: str
    amount: float
    date: int
    bank_name: str
    payment_proportion: float = 1.0
    transaction_type: str = "debit"
    subcategory_id: int
    classification_id: int
    account_id: int


class ClassifySchemas(BaseModel):
    name: str


class CreateSubCategory(BaseModel):
    name: str
    category_id: int


class TransactionBaseModel(BaseModel):
    class_name: str
    category_name: str
    subcategory_name: str
    amount: float
    pay_ratio: int


class CreateInstitutionModel(BaseModel):
    name: str


class CreateBankAccount(BaseModel):
    account_type: str
    name: str
    amount: float
    banking_institution_id: int
