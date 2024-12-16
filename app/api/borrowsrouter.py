

from typing import Annotated, Optional

from core.errors import APIException
from core.models import Borrow, db_helper
from core.schemas import BorrowCreate, BorrowRead, BorrowReturn, BorrowsListBase
from core.schemas.error import ErrorBase
from fastapi import APIRouter, Depends
from fastapi.exceptions import ResponseValidationError
from sqlalchemy.ext.asyncio import AsyncSession

from api.crud import borrows_crud
from api.crud.borrows import BorrowsCrud

router = APIRouter(tags=["Borrows"])

router.responses = {
    404: {"model": ErrorBase, "description": "Not Found"},
}

@router.get("", response_model=BorrowsListBase)
async def get_borrows_list(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    page: int = 0,
    per_page: int = 15,
):
    borrows = await borrows_crud.get_all_items(
        session=session,
        page=page,
        per_page=per_page,
    )
    borrows = [b.__dict__ for b in borrows]
    result = BorrowsListBase(
        items_list=borrows,
        page=page,
        per_page=per_page,

    )
    return result

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
