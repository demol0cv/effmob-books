

from fastapi import APIRouter

router = APIRouter(tags=["Borrows"])



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
