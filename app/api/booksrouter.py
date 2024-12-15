from typing import Annotated

import sqlalchemy.exc
from fastapi import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from api.crud import books_crud
from core.errors import APIException
from core.models import db_helper, Book
from core.schemas.book import BookRead, BookCreate, BookBase, BookUpdate
from core.schemas.error import ErrorBase
from fastapi import APIRouter, Depends, HTTPException

router = APIRouter(tags=["Books"])
router.responses = {
    404: {"model": ErrorBase, "description": "Not Found"}
}


@router.get("", response_model=list[BookRead])
async def get_books_list(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        offset: int = 0,
        limit: int = 15,
):
    books = await books_crud.get_all_items(
        session=session,
        offset=offset,
        limit=limit,
    )
    return books

@router.get("/{id}", response_model=BookRead)
async def get_book_info(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        id: int,
) -> Book | None:
    book = await books_crud.get_one_item(
        session=session,
        id=id,
    )
    return book

@router.post("", response_model=BookCreate)
async def add_book(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        book: BookCreate,
) -> Book:
    book = await books_crud.create_book(
        session=session,
        book_create=book,
    )
    return book


@router.put("/{id}", response_model=BookBase)
async def update_book(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        id: int,
        book_update: BookUpdate,
):
    book = await books_crud.update_book(
        session=session,
        id=id,
        book_update=book_update,
    )
    return book

@router.delete("{id}")
async def remove_book(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    id: int,
    ):
    book = await books_crud.remove_item(
        session=session,
        id=id,
    )
    return book
