from abc import ABC, abstractmethod
from collections.abc import Sequence

from api.crud.basecrud import CRUDBase
from core.models import Author
from core.schemas.author import AuthorBase, AuthorCreate, AuthorRead, AuthorUpdate
from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession




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
