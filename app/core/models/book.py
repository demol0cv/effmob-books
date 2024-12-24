from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship, sessionmaker

from .author import Author
from .base import Base


class Book(Base):
    name: Mapped[str]
    description: Mapped[str]
    author_id: Mapped[int]
    count: Mapped[int]

    author = relationship(Author, back_populates="book")
