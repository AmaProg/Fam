from pydantic import BaseModel


class AccountBM(BaseModel):
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
    subcategory_id: int
    classification_id: int
    account_id: int


class CreateClassify(BaseModel):
    name: str


class CreateSubCategory(BaseModel):
    name: str
    category_id: int
