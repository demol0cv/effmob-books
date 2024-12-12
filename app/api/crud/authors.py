import abc
from typing import Sequence

from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Author
from core.schemas.author import AuthorCreate, AuthorRead, AuthorUpdate


class AuthorsCrud(abc.ABC):
    async def get_authors(
            session: AsyncSession,
            offset: int = 0,
            limit: int = 15
            ) -> Sequence[Author]:
        query = select(Author).order_by(Author.last_name).offset(offset).limit(limit)
        result = await session.scalars(query)
        return result.all()

    async def get_one_author(
            session: AsyncSession,
            author_id: int,
                            ) -> Author | None:
        query = select(Author).where(Author.id == author_id)
        result = await session.scalars(query)
        return result.one_or_none()

    async def create_author(
            session: AsyncSession,
            author_create: AuthorCreate,
    ) -> Author:
        author = Author(**author_create.model_dump())
        session.add(author)
        await session.commit()
        return author

    async def remove_author(
            session: AsyncSession,
            author_id: int,
    ) -> Author:
        select_query = select(Author).where(Author.id == author_id)
        result = await session.execute(select_query)
        author = result.scalar_one_or_none()
        if author is not None:
            delete_query = delete(Author).where(Author.id == author.id)
            await session.execute(delete_query)
            await session.commit()
        
        return author

    async def update_author(
            session: AsyncSession,
            author_id: int,
            author_update: AuthorUpdate,
    )-> Author:
        select_query = select(Author).where(Author.id == author_id)
        result = await session.execute(select_query)
        author = result.scalar_one_or_none()

        if author is not None:
            update_query = update(Author).where(Author.id == author_id).values(**author_update.model_dump())
            await session.execute(update_query)
            await session.commit()
            select_query = select(Author).where(Author.id == author_id)
            result = await session.execute(select_query)
            author = result.scalar_one_or_none()

        return author

