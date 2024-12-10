from datetime import datetime

from pydantic import BaseModel


class AuthorBase(BaseModel):
    first_name: int
    last_name: str
    birthdate: datetime

class AuthorCreate(AuthorBase):
    pass

class AuthorRead(AuthorBase):
    id: int

