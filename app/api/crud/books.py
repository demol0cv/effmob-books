from abc import ABC, abstractmethod
from collections.abc import Sequence

from .basecrud import CRUDBase
from core.errors import APIException
from core.models import Book
from core.schemas.book import BookCreate, BookUpdate
from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

__all__ = [
    "BooksCrud",
]
class BooksCrud(CRUDBase):
    async def create_book(
            self,
            session: AsyncSession,
            book_create: BookCreate,
    ) -> Book:
        book = Book(**book_create.model_dump())
        session.add(book)
        await session.commit()
        return book


    async def update_book(
            self,
            session: AsyncSession,
            book_id: int,
            book_update: BookUpdate,
    ) -> Book | None:

        result = await session.execute(
            select(Book).where(Book.id == book_id),
        )
        book_for_update = result.scalar_one_or_none()
        if not book_for_update:
            raise APIException(
                code=404,
                error="Book not found",
                details=f"Книга с ID = {book_id} не найдена",
            )
        new_data = book_update.model_dump(exclude_unset=True)
        if not new_data:
            raise APIException(
                code=400,
                error="No data for update",
                details=f"Нет данных для обновления",
            )
        for key, value in new_data.items():
            setattr(book_for_update, key, value)
        await session.commit()
        result = await session.execute(
            select(Book).where(Book.id == book_id),
        )
        result = result.scalar_one_or_none()
        return result

        
        #return result.scalar_one_or_none()

