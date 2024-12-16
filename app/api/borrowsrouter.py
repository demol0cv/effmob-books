

from typing import Annotated, Optional
from fastapi import APIRouter, Depends
from fastapi.exceptions import ResponseValidationError
from sqlalchemy.ext.asyncio import AsyncSession

# from api.crud.borrows import BorrowsCrud
from api.crud import borrows_crud
from api.crud.borrows import BorrowsCrud
from core.errors import APIException
from core.models.borrow import Borrow
from core.schemas.borrow import BorrowCreate, BorrowRead, BorrowReturn
from core.models import db_helper
from core.schemas.error import ErrorBase

router = APIRouter(tags=["Borrows"])

router.responses = {
    404: {"model": ErrorBase, "description": "Not Found"},
}

@router.get("", response_model=list[BorrowRead])
async def get_borrows_list(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    offset: int = 0,
    limit: int = 15,
):
    borrows = await borrows_crud.get_all_items(
        session=session,
        offset=offset,
        limit=limit,
    )
    return borrows

@router.get("/{id}", response_model=Optional[BorrowRead])
async def get_borrow_info(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    id: int,
):
    borrow = await borrows_crud.get_one_item(
        session=session,
        id=id,
    )
    return borrow

@router.post("", response_model=Optional[BorrowCreate])
async def add_borrow(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    borrow_create: BorrowCreate,
) -> Borrow:
    new_borrow = await borrows_crud.create_borrow(
        session=session,
        borrow_create=borrow_create,
    )
    return new_borrow

@router.patch("/{id}/return", response_model=Optional[BorrowReturn])
async def return_borrow(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    id: int,
    borrow_return: BorrowReturn,
):
    borrow = await borrows_crud.borrow_return(
        session=session,
        id=id,
        borrow_return=borrow_return,
    )
    return borrow
