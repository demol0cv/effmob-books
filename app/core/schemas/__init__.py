__all__= [
    "ApiError",
    "AuthorCreate",
    "AuthorRead",
    "AuthorUpdate",
    "BookCreate",
    "BookRead",
    "BookUpdate",
    "BorrowCreate",
    "BorrowRead",
    "BorrowReturn",
    "FakeBase",
]

from .author import AuthorCreate, AuthorRead, AuthorUpdate
from .book import BookCreate, BookRead, BookUpdate
from .borrow import BorrowCreate, BorrowRead, BorrowReturn
from .error import ApiError
