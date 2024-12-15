from typing import Annotated

import sqlalchemy.exc
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from api.crud import authors_crud
from core.errors import APIException
from core.models import db_helper, Author
from core.schemas.author import AuthorRead, AuthorCreate, AuthorUpdate
from core.schemas.error import ErrorBase

router = APIRouter(tags=["Authors"])
router.responses = {
    404: {"model": ErrorBase, "description": "Not Found"}
}


@router.get("", response_model=list[AuthorRead])
async def get_authors_list(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        offset: int = 0,
        limit: int = 15,
):
    authors = await authors_crud.get_all_items(
        session=session,
        offset=offset,
        limit=limit
    )
    return authors

@router.get("/{id}", response_model=AuthorRead)
async def get_author_info(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        id: int
):
    try:
        author = await authors_crud.get_one_item(
            session=session,
            id=id,
        )
        return author
    except sqlalchemy.exc.NoResultFound:
        raise APIException(
            code=404,
            error="Author not found",
            details=f"Author with id={id} not found"
        )

@router.post("", response_model=AuthorCreate)
async def add_author(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        author: AuthorCreate,
) -> Author:
    author = await authors_crud.create_author(
        session=session,
        author_create=author
    )
    
    return author
    

@router.put("/{id}", response_model=AuthorUpdate)
async def update_author(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    id: int,
    author_update: AuthorUpdate,
    )-> Author:
    author = await authors_crud.update_author(
        session=session,
        id=id,
        author_update=author_update,
    )
    if author:
        return author
    else:
        raise APIException(
            code=404,
            error="Автор не найден",
            details=f"Автор с ID {id} не найден"
        )

@router.delete("/{id}", response_model=AuthorUpdate)
async def remove_author(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    id: int,
) -> Author:
    author = await authors_crud.remove_item(
        session=session,
        id=id,
    )
    if author:
        return author
    else:
        raise APIException(
            code=404,
            error="Автор не найден",
            details=f"Автор с ID {id} не найден",
        )
