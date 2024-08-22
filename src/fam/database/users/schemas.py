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
    amount: float
    date: int
    account_id: int
    subcategory_id: int
    classification_id: int


class CreateClassify(BaseModel):
    name: str


class CreateSubCategory(BaseModel):
    name: str
    category_id: int
