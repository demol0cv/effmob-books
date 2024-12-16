from typing import Annotated, Optional, Sequence

from pydantic import Field
import sqlalchemy.exc
from core.errors import APIException
from core.models import Book, db_helper
from core.models.base import Base
from core.schemas import ApiError, BookCreate, BookRead, BookUpdate
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from api.crud import books_crud
from core.schemas import BooksListRead

router = APIRouter(tags=["Books"])
router.responses = {
    404: {"model": ApiError, "description": "Not Found"}
}


@router.get("", response_model=BooksListRead)
async def get_books_list(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        page: int = 0,
        per_page: int = 15,
) -> Sequence[Base]:
    books = await books_crud.get_all_items(
        session=session,
        page=page,
        per_page=per_page,
    )
    result = BooksListRead(
        items_list=[b.__dict__ for b in books],
        page=page,
        per_page=per_page,
    )
    return result

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
