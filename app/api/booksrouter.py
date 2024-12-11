

from fastapi import APIRouter

from core.schemas.error import ErrorBase

router = APIRouter(tags=["Books"])
router.responses = {
    404: {"model": ErrorBase, "description": "Not Found"}
}
authors = ["author1", "author2", "author3", "author4", "author5"]

books = ["book1", "book2", "book3", "book4", "book5"]

@router.get("")
async def get_books_list():
    return books

@router.get("/{id}")
async def get_book_info(id: int):
    return books[id]

@router.post("/{book_name}")
async def add_book(book_name: str):
    if book_name not in books:
        books.append(book_name)

@router.put("")
async def update_book(id: int, new_name: str):
    books[id] = new_name

@router.delete("{id}")
async def remove_book(id: int):
    if id >=0 and id < len(books):
        return books.pop(id)
