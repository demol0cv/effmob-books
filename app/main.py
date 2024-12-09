import uvicorn
from fastapi import FastAPI
from contextlib import asynccontextmanager

from api import router
from core.config import settings
from core.models import db_helper

@asynccontextmanager
async def lifespan(app: FastAPI):
    # start
    yield
    # stop
    await db_helper.dispose()

main_app = FastAPI(
    lifespan=lifespan,
)
main_app.include_router(
    router,
    prefix=settings.api.prefix
)


if __name__ == "__main__":
    uvicorn.run(
        "main:main_app",
        host=settings.run.host,
        port=settings.run.port,
        reload=True,
        )
