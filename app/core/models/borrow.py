from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column


from .base import Base

class Borrow(Base):
    book_id: Mapped[int]
    reader_name: Mapped[str]
    borrow_date: Mapped[datetime]
    return_date: Mapped[datetime]
