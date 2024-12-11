from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Author
from core.schemas.author import AuthorCreate, AuthorRead


async def get_authors(session: AsyncSession, offset: int = 0, limit: int=5) -> Sequence[Author]:
    query = select(Author).order_by(Author.last_name).offset(offset).limit(limit)
    result = await session.scalars(query)
    return result.all()

async def get_one_author(
        session: AsyncSession,
        author_id: int,
                         ) -> Author:
    query = select(Author).where(Author.id == author_id)
    result = await session.scalars(query)
    return result.one()

async def create_author(
        session: AsyncSession,
        author_create: AuthorCreate,
) -> Author:
    author = Author(**author_create.model_dump())
    session.add(author)
    await session.commit()
    return author
