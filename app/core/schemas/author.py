from datetime import datetime, date

from pydantic import BaseModel, Field
from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import TIMESTAMP

from .base import ItemBase


class AuthorBase(ItemBase):
    first_name: str = Field(example="Name")
    last_name: str = Field(example="LastName")
    birthdate: date

class AuthorCreate(AuthorBase):
    pass

class AuthorRead(AuthorBase):
    id: int

class AuthorUpdate(AuthorBase):
    pass
