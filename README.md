## Архитерктура
В проекте применяется подход Clean Architecture
## Links
- https://docs.sqlalchemy.org/en/20/core/engines.html
- https://fastapi.tiangolo.com/advanced/events/#lifespan
- https://alembic.sqlalchemy.org/en/latest/cookbook.html#using-asyncio-with-alembic

## Запуск
Выполнить:
```bash
docker-compose up --build
```
Остановить нажав Ctrl+C
и снова запустить - выполнится миграция данных и создадутся таблицы (это проблема, нужно дорабатывать сценарий запуска миграции)
Подключение к postgres: admin:adminpass@db:5432/effmob-books-db
### Fake data
После успешного запуска и выполнения миграций, выполнить:
```bash
docker exec effmob_books python3 /app/fill_db.py
```
чтобы заполнить таблицы фейковыми данными. Заполнятся таблицы authors и books

## Приложение
- swagger: http://0.0.0.0:8000/docs#/
- api: http://0.0.0.0:8000/api/


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
