from pydantic import BaseModel

from core.models.book import Book

from .base import ItemBase, ListItemsBase


class BookBase(ItemBase):
    name: str
    description: str
    author_id: int
    count: int

class ListBooksBase(ListItemsBase):
    items_list: list[BookBase]


class BooksListRead(ListBooksBase):
    pass


class BookCreate(BookBase):
    pass

class BookRead(BookBase):
    pass

class BookUpdate(BookBase):
    pass