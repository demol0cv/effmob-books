from abc import ABC, abstractmethod
from collections.abc import Sequence

from core.errors import APIException
from core.models import Book
from core.models.borrow import Borrow
from core.schemas.borrow import BorrowCreate, BorrowReturn
from sqlalchemy import and_, delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from .basecrud import CRUDBase

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
            if book.count > 0:
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

    async def borrow_return(
        self,
        session: AsyncSession,
        id: int,
        borrow_return: BorrowReturn,
    ):
        request = await session.execute(
            select(Borrow).where(
                and_(
                    Borrow.id == id,
                    Borrow.is_active == True,
                ),
            ),
        )
        borrow_for_update = request.scalar_one_or_none()

        if borrow_for_update is not None:
            await session.execute(
                update(Borrow)
                .where(
                    Borrow.id == id,
                )
                .values(
                    **borrow_return.model_dump(
                        exclude_none=True,
                    )
                ),
            )

            book_request = await session.execute(
                select(Book).where(
                    Book.id == borrow_for_update.book_id,
                ),
            )
            book_request = book_request.scalar_one_or_none()
            book_request.count += 1

            await session.commit()

            return_request = await session.execute(
                select(Borrow).where(Borrow.id == id),
            )
            return_request = return_request.scalar_one_or_none()
            return return_request

        return None
