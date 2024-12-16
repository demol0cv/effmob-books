import os

from pydantic import BaseModel, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseConfig(BaseModel):
    """Конфигурация БД."""

    url: PostgresDsn
    echo: bool = False
    echo_pool: bool = False
    pool_size: int = 50
    max_overflow: int = 10

class RunConfig(BaseModel):
    """Конфигурация запуска."""

    host: str = "0.0.0.0"
    port: int = 8000

class ApiPrefix(BaseModel):
    """Конфигурация API."""

    prefix: str = "/api"
    books: str = "/books"
    authors: str = "/authors"
    borrows: str = "/borrows"

class Settings(BaseSettings):
    """Общая конфигурация."""

    run: RunConfig = RunConfig()
    api: ApiPrefix = ApiPrefix()
    db: DatabaseConfig

    model_config = SettingsConfigDict(
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="APP_CONFIG__",
        env_file=".env",
    )



settings = Settings()
