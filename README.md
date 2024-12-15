## Архитерктура
В проекте применяется подход Clean Architecture
## Links
- https://docs.sqlalchemy.org/en/20/core/engines.html
- https://fastapi.tiangolo.com/advanced/events/#lifespan
- https://alembic.sqlalchemy.org/en/latest/cookbook.html#using-asyncio-with-alembic

## Приложение
- swagger: http://0.0.0.0:8000/docs#/
- api: http://0.0.0.0:8000/api/
- 

## Эндпоинты
### Эндпоинты для книг:
- Добавление книги (POST /books).
- Получение списка книг (GET /books).
- Получение информации о книге по id (GET /books/{id}).
- Обновление информации о книге (PUT /books/{id}).
- Удаление книги (DELETE /books/{id}).

### Эндпоинты для авторов:
- Создание автора (POST /authors).
- Получение списка авторов (GET /authors).
- Получение информации об авторе по id (GET /authors/{id}).
- Обновление информации об авторе (PUT /authors/{id}).
- Удаление автора (DELETE /authors/{id}).

### Эндпоинты для выдач:
- Создание записи о выдаче книги (POST /borrows).
- Получение списка всех выдач (GET /borrows).
- Получение информации о выдаче по id (GET /borrows/{id}).
- Завершение выдачи (PATCH /borrows/{id}/return) с указанием даты возврата.
