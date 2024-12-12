from typing import Annotated

import sqlalchemy.exc
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from api.crud import AuthorsCrud
from core.errors import APIException
from core.models import db_helper, Author
from core.schemas.author import AuthorRead, AuthorCreate, AuthorUpdate
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
    authors = await AuthorsCrud.get_authors(
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
        author = await AuthorsCrud.get_one_author(
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
    author = await AuthorsCrud.create_author(
        session=session,
        author_create=author
    )
    return author

@router.put("/{author_id}", response_model=AuthorUpdate)
async def update_author(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    author_id: int,
    author_update: AuthorUpdate,
    )-> Author:
    author = await AuthorsCrud.update_author(
        session=session,
        author_id=author_id,
        author_update=author_update,
    )
    return author

@router.delete("/{id}")
async def remove_author(id:int):
    return authors.pop(id)
