from typing import Optional
from fastapi import APIRouter
from pydantic import Field

from fill_db import DbUtils


router = APIRouter(tags=["Fake"])

@router.get("/fake",
            summary="Заполнить БД фэйковыми данными",
            description="Эндпоинт заполняет БД фэйковыми данным книг и авторов."
            )
async def fill_fake_data(
    authors_count: Optional[int] = None,
    books_count: Optional[int] = None,
):
    await DbUtils().fill_fake_data(authors_count=authors_count, books_count=books_count)
