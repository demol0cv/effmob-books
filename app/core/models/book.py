from sqlalchemy.orm import Mapped, mapped_column


from .base import Base

class Book(Base):
    name: Mapped[str]
    description: Mapped[str]
    author_id: Mapped[int]
    count: Mapped[int]
