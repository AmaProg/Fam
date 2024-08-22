from pydantic import BaseModel


class CreateUser(BaseModel):
    email: str
    password: str
    database_url: str
