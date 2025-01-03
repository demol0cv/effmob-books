__all__ = [
    "authors_crud",
    "books_crud",
    "borrows_crud",
]

from core.models.author import Author
from core.models.book import Book
from core.models.borrow import Borrow
from .cruds import AuthorsCrud, BorrowsCrud, BooksCrud


authors_crud = AuthorsCrud(Author)
books_crud = BooksCrud(Book)
borrows_crud = BorrowsCrud(Borrow)
