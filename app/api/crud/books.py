import abc
from typing import Sequence
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from core.errors import APIException
from core.models import Book
from core.schemas.book import BookCreate, BookUpdate

__all__ = [
    "BooksCrud"
]
class BooksCrud(abc.ABC):
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
        return result.one_or_none()

    async def create_book(
            session: AsyncSession,
            book_create: BookCreate,
    ) -> Book:
        book = Book(**book_create.model_dump())
        session.add(book)
        await session.commit()
        return book

    async def update_book(
            session: AsyncSession,
            book_id: int,
            book_update: BookUpdate,
    ):

        result = await session.execute(
            select(Book).where(Book.id == book_id)
        )
        book_for_update = result.scalar_one_or_none()
        if not book_for_update:
            raise APIException(
                code=404,
                error="Book not found",
                details=f"Книга с ID = {book_id} не найдена"
            )
        new_data = book_update.model_dump(exclude_unset=True)
        if not new_data:
            raise APIException(
                code=400,
                error="No data for update",
                details=f"Нет данных для обновления"
            )
        for key, value in new_data.items():
            setattr(book_for_update, key, value)
        await session.commit()
        result = await session.execute(
            select(Book).where(Book.id == book_id)
        )
        result = result.scalar_one_or_none()
        return result
    
    async def remove_book(
            session: AsyncSession,
            book_id: int
            ) -> Book:
        """
        docstring
        """
        select_query = select(Book).where(Book.id == book_id)
        result = await session.execute(select_query)
        book = result.scalar_one_or_none()
        if book is not None:
            delete_query = delete(Book).where(Book.id == book_id)
            await session.execute(delete_query)
            await session.commit()
        
        return book
        
        #return result.scalar_one_or_none()

