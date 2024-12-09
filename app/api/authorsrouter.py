

from fastapi import APIRouter

router = APIRouter(tags=["Authors"])

authors = ["author1", "author2", "author3", "author4", "author5"]

@router.get("")
async def get_authors_list():
    return authors

@router.get("/{id}")
async def get_author_info(id: int):
    return authors[id]

@router.post("/{author_name}")
async def add_author(author_name: str):
    authors.append(author_name)

@router.put("/{id}")
async def update_author(id: int, new_name: str):
    authors[id] = new_name

@router.delete("/{id}")
async def remove_author(id:int):
    return authors.pop(id)
