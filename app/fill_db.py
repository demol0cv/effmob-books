import asyncio
import random
from api.crud import authors_crud
from core.models import Author, db_helper
from faker import Faker
from faker.providers import lorem
from sqlalchemy import select

from core.models.book import Book
from core.schemas.author import AuthorCreate
from core.schemas.book import BookCreate

fake = Faker()
fake.add_provider(lorem)

book_title =lambda: " ".join(fake.words(nb=3)).title()
description = lambda: " ".join(fake.words(nb=15)).capitalize()

class DbUtils:
    async def fill_fake_data():
        async with db_helper.session_factory() as sess:
            for _ in range(53):
                name = fake.first_name()
                last_name = fake.last_name()
                birthday = fake.date_of_birth(minimum_age=20)
                author = Author(
                    **AuthorCreate(
                        first_name=name,
                        last_name=last_name,
                        birthdate=birthday,
                    ).model_dump(),
                )
                sess.add(author)
            await sess.commit()
            query = select(Author.id)
            result = await sess.execute(query)
            author_ids = result.scalars().all()
            for _ in range(300):
                name = book_title
                book = Book(
                    **BookCreate(
                        author_id=random.choice(author_ids),
                        count=random.randint(10,30),
                        description=description(),
                        name=book_title(),
                    ).model_dump()
                )
                sess.add(book)
            await sess.commit()


if __name__ == "__main__":
    dbu = DbUtils()
    asyncio.run(dbu.fill_fake_data())
