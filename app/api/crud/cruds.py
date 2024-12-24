from abc import ABC, abstractmethod
from collections.abc import Sequence

from core.errors import APIException
from core.models import Author
from core.models.base import Base
from core.models.book import Book
from core.models.borrow import Borrow
from core.schemas.author import AuthorBase, AuthorCreate, AuthorRead, AuthorUpdate
from core.schemas.base import ItemBase
from core.schemas.book import BookCreate, BookUpdate
from core.schemas.borrow import BorrowCreate, BorrowReturn
from sqlalchemy import and_, delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession


class CRUDBase:
    def __init__(self, model:Base):
        self.model = model

    async def get_one_item(
            self,
            session: AsyncSession,
            id: int,
    ) -> Base | None:
        query = select(self.model).where(self.model.id == id)

        result = await session.execute(query)

        item = result.scalar_one_or_none()
        return item
    

    async def get_all_items(
            self,
            session: AsyncSession,
            page: int = 0,
            per_page: int = 15,
    ) -> Sequence[Base]:
        offset = page*per_page
        query = select(self.model).order_by(self.model.id).offset(offset).limit(per_page)
        result = await session.scalars(query)
        return result.all()
    
    async def create_item(
            self,
            session: AsyncSession,
            item_create: ItemBase,
    ) -> Base:
        item = ItemBase(**item_create.model_dump())
        session.add(item)
        await session.commit()
        return item
    
    async def remove_item(
            self,
            session: AsyncSession,
            id: int,
    ) -> Base:
        select_query = select(self.model).where(self.model.id == id)
        result = await session.execute(select_query)
        item = result.scalar_one_or_none()
        if item is not None:
            delete_query = delete(self.model).where(self.model.id == item.id)
            await session.execute(delete_query)
            await session.commit()
        
        return item
        

class AuthorsCrud(CRUDBase):
    async def update_author(
            self,
            session: AsyncSession,
            id: int,
            author_update: AuthorUpdate,
    )-> Author:
        select_query = select(Author).where(Author.id == id)
        result = await session.execute(select_query)
        author = result.scalar_one_or_none()

        if author is not None:
            update_query = update(Author).where(Author.id == id).values(**author_update.model_dump())
            await session.execute(update_query)
            await session.commit()
            select_query = select(Author).where(Author.id == id)
            result = await session.execute(select_query)
            author = result.scalar_one_or_none()

        return author

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
                    ),
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
