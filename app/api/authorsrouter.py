from typing import Annotated

import sqlalchemy.exc
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from api.crud.authors import get_authors, create_author, get_one_author
from core.errors import APIException
from core.models import db_helper, Author
from core.schemas.author import AuthorRead, AuthorCreate
from core.schemas.error import ErrorBase

router = APIRouter(tags=["Authors"])
router.responses = {
    404: {"model": ErrorBase, "description": "Not Found"}
}
authors = ["author1", "author2", "author3", "author4", "author5"]

@router.get("", response_model=list[AuthorRead])
async def get_authors_list(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        offset: int = 0,
        limit: int = 15,
):
    authors = await get_authors(
        session=session,
        offset=offset,
        limit=limit
    )
    return authors

@router.get("/{id}", response_model=AuthorRead)
async def get_author_info(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        author_id: int
):
    try:
        author = await get_one_author(
            session=session,
            author_id=author_id
        )
        return author
    except sqlalchemy.exc.NoResultFound:
        raise APIException(
            code=404,
            error="Author not found",
            details=f"Author with id={author_id} not found"
        )

@router.post("", response_model=AuthorCreate)
async def add_author(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        author: AuthorCreate,
) -> Author:
    author = await create_author(
        session=session,
        author_create=author
    )
    return author

@router.put("/{id}")
async def update_author(id: int, new_name: str):
    authors[id] = new_name

@router.delete("/{id}")
async def remove_author(id:int):
    return authors.pop(id)
