from pydantic import BaseModel


class AccountBM(BaseModel):
    account_name: str
    description: str


class CategoryBM(BaseModel):
    category_name: str
    description: str
