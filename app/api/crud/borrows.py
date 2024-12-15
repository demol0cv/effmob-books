from abc import ABC, abstractmethod
from collections.abc import Sequence

from .basecrud import CRUDBase
from core.errors import APIException
from core.models import Book
from core.models.borrow import Borrow
from core.schemas.borrow import BorrowCreate
from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

__all__ = [
    "BooksCrud",
]

class BorrowsCrud(CRUDBase):
    async def create_borrow(
        self,
        session: AsyncSession,
        borrow_create: BorrowCreate,
    ) -> Borrow:
        new_borrow = Borrow(**borrow_create.model_dump())
        query_book = select(Book).where(Book.id == new_borrow.book_id)
        result = await session.execute(query_book)
        book = result.scalar_one_or_none()
        if book is not None:
            if book.count>0:
                book.count -= 1
                session.add(new_borrow)
                await session.commit()
                return new_borrow
            else:
                raise APIException(
                    code=404,
                    error="Не хватает книг",
                    details="Недостаточное количество книг",
                )
        return None

    

