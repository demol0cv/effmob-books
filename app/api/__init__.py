__all__ = [
    "router",
]

from core.config import settings
from fastapi import APIRouter

from .authorsrouter import router as authors_router
from .booksrouter import router as books_router
from .borrowsrouter import router as borrows_router
from .fakerouter import router as fake_router

router = APIRouter(
    prefix=settings.api.prefix,
)

router.include_router(
    books_router,
    prefix=settings.api.books,
)

router.include_router(
    authors_router,
    prefix=settings.api.authors,
)

router.include_router(
    borrows_router,
    prefix=settings.api.borrows,
)

router.include_router(
    fake_router,
    prefix="/fake",
)
