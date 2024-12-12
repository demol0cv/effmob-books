from typing import Annotated

import sqlalchemy.exc
from fastapi import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from api.crud import BooksCrud
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
    books = await BooksCrud.get_all_books(
        session=session,
        offset=offset,
        limit=limit,
    )
    return books

@router.get("/{book_id}", response_model=BookRead)
async def get_book_info(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        book_id: int,
):
    try:
        book = await BooksCrud.get_one_book(
            session=session,
            book_id=book_id,
        )
        return book
    except sqlalchemy.exc.NoResultFound:
        raise APIException(
            code=404,
            error="Book not found",
            details=f"Book with id={book_id} not found"
        )

@router.post("", response_model=BookCreate)
async def add_book(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        book: BookCreate,
) -> Book:
    book = await BooksCrud.create_book(
        session=session,
        book_create=book,
    )
    return book


@router.put("/{book_id}", response_model=BookBase)
async def update_book(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        book_id: int,
        book_update: BookUpdate,
):
    book = await BooksCrud.update_book(
        session=session,
        book_id=book_id,
        book_update=book_update,
    )
    return book

@router.delete("{book_id}")
async def remove_book(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    book_id: int,
    ):
    book = await BooksCrud.remove_book(
        session=session,
        book_id=book_id,
    )
    return book
