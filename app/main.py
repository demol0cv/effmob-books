import uvicorn
from fastapi import FastAPI


from api import books_router
from core.config import settings


app = FastAPI()
app.include_router(
    books_router,
    prefix=settings.api.prefix,
)

@app.post("/authors")
def add_author():
    """Создание автора."""
    pass

@app.get("/authors")
def get_authors():
    """Получение списка авторов."""
    return ["Author 1", "Author 2", "Author 3"]

@app.get("/authors/{id}")
def get_author(id: int):
    """Получение информации об авторе.

    Args:
        id (int): ID автора

    """
    pass

@app.put("/authors/{id}")
def update_author(id: int):
    """Обновление информации об авторе.

    Args:
        id (int): ID автора

    """
    pass

@app.delete("/authors/{id}")
def del_author(id: int):
    """Удаление автора.

    Args:
        id (int): id автора

    """
    pass



def add_book():
    pass

def get_books():
    pass

def get_book(id: int):
    pass

def del_book(id: int):
    pass

def add_borrow():
    pass

def get_borrows():
    pass

def get_borrow(id: int):
    pass

def end_borrow(id: int):
    pass

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.run.host,
        port=settings.run.port,
        reload=True,
        )
