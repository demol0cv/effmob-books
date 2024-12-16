from typing import Annotated, Optional

import sqlalchemy.exc
from core.errors import APIException
from core.models import Book, db_helper
from core.schemas import ApiError, BookCreate, BookRead, BookUpdate
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from api.crud import books_crud

router = APIRouter(tags=["Books"])
router.responses = {
    404: {"model": ApiError, "description": "Not Found"}
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

@router.get("/{id}", response_model=Optional[BookRead])
async def get_book_info(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        id: int,
) -> Book | None:
    book = await books_crud.get_one_item(
        session=session,
        id=id,
    )
    return book

@router.post("", response_model=Optional[BookCreate])
async def add_book(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        book: BookCreate,
) -> Book:
    book = await books_crud.create_book(
        session=session,
        book_create=book,
    )
    return book


@router.put("/{id}", response_model=Optional[BookUpdate])
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

@router.delete("/{id}", response_model=Optional[BookRead])
async def remove_book(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    id: int,
    ):
    book = await books_crud.remove_item(
        session=session,
        id=id,
    )
    return book
