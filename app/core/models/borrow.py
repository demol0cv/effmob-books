from datetime import date, datetime

from sqlalchemy.orm import Mapped, mapped_column


from .base import Base

class Borrow(Base):
    book_id: Mapped[int]
    reader_name: Mapped[str]
    is_active: Mapped[bool]
    borrow_date: Mapped[date]
    return_date: Mapped[date|None] = mapped_column(default=None, nullable=True)
