from datetime import datetime, date

from pydantic import BaseModel
from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import TIMESTAMP


class AuthorBase(BaseModel):
    first_name: str
    last_name: str
    birthdate: date

class AuthorCreate(AuthorBase):
    pass

class AuthorRead(AuthorBase):
    id: int

class AuthorUpdate(AuthorBase):
    pass
