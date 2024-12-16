from pydantic import BaseModel

from .base import ItemBase


class BookBase(ItemBase):
    name: str
    description: str
    author_id: int
    count: int


class BookCreate(BookBase):
    pass

class BookRead(BookBase):
    id: int

class BookUpdate(BookBase):
    pass