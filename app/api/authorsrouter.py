from typing import Annotated, Optional

import sqlalchemy.exc
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from api.crud import authors_crud
from core.errors import APIException
from core.models import db_helper, Author
from core.schemas import AuthorRead, AuthorCreate, AuthorUpdate
from core.schemas import ApiError
from core.schemas.author import ListAuthorsBase

router = APIRouter(tags=["Authors"])
router.responses = {
    404: {"model": ApiError, "description": "Not Found"}
}


@router.get("", response_model=ListAuthorsBase)
async def get_authors_list(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        page: int = 0,
        per_page: int = 15,
):
    authors = await authors_crud.get_all_items(
        session=session,
        page=page,
        per_page=per_page
    )
    result = ListAuthorsBase(
        items_list=[a.__dict__ for a in authors],
        page=page,
        per_page=per_page,
    )   
    return result

@router.get("/{id}", response_model=Optional[AuthorRead])
async def get_author_info(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        id: int
):
    author = await authors_crud.get_one_item(
        session=session,
        id=id,
    )
    return author


@router.post("", response_model=Optional[AuthorCreate])
async def add_author(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        author: AuthorCreate,
) -> Author:
    author = await authors_crud.create_author(
        session=session,
        author_create=author
    )
    
    return author
    

@router.put("/{id}", response_model=Optional[AuthorUpdate])
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
    return author


@router.delete("/{id}", response_model=Optional[AuthorUpdate])
async def remove_author(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    id: int,
) -> Author:
    author = await authors_crud.remove_item(
        session=session,
        id=id,
    )
    return author
