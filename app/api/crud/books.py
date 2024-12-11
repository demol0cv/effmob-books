from typing import Sequence
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from core.models import Book
from core.schemas.book import BookCreate


async def get_all_books(
        session: AsyncSession,
        offset: int = 0,
        limit: int = 15
) -> Sequence[Book]:
    query = select(Book).order_by(Book.name).offset(offset).limit(limit)
    result = await session.scalars(query)
    return result.all()

async def get_one_book(
        session: AsyncSession,
        book_id: int,
) -> Book:
    query = select(Book).where(Book.id == book_id)
    result = await session.scalars(query)
    return result.one()

async def create_book(
        session: AsyncSession,
        book_create: BookCreate,
) -> Book:
    book = Book(**book_create.model_dump())
    session.add(book)
    await session.commit()
    return book
