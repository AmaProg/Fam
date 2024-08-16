from pydantic import BaseModel


class CreateUser(BaseModel):
    first_name: str
    last_name: str
    password: str
    database_url: str
