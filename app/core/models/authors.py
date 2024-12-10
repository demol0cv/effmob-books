from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column


from .base import Base

class Author(Base):
    first_name: Mapped[int]
    last_name: Mapped[str]
    birthdate: Mapped[datetime]
