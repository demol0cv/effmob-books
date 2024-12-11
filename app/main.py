import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager

from api import router
from core.config import settings
from core.errors import APIException
from core.models import db_helper
from core.schemas.error import ErrorBase


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
    router
)

@main_app.exception_handler(APIException)
async def api_exception_handler(request: Request, exc: APIException):
    response_data = ErrorBase(
        code=exc.code,
        error=exc.error,
        details=exc.details
    )
    return JSONResponse(
        status_code=exc.code,
        content=response_data.dict()
    )

if __name__ == "__main__":
    uvicorn.run(
        "main:main_app",
        host=settings.run.host,
        port=settings.run.port,
        reload=True,
        )
