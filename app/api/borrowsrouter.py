

from fastapi import APIRouter

from core.schemas.error import ErrorBase

router = APIRouter(tags=["Borrows"])
router.responses = {
    404: {"model": ErrorBase, "description": "Not Found"}
}
authors = ["author1", "author2", "author3", "author4", "author5"]


@router.get("")
async def get_borrows_list():
    pass

@router.get("")
async def get_borrow_info():
    pass

@router.post("")
async def add_borrow():
    pass

@router.patch("")
async def return_borrow():
    pass
