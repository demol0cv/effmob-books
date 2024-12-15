FROM python:3.12.7-slim


WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONNUNBUFFERED=1
ENV APP_CONFIG__DB__URL=postgresql+asyncpg://admin:adminpass@db:5432/effmob-books-db

COPY ./app/requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

copy ./app /app/

CMD alembic upgrade head && python3 /app/main.py