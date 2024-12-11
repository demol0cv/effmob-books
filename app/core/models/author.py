from datetime import datetime, date

from sqlalchemy import DateTime, Column
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column


from .base import Base

class Author(Base):
    first_name: Mapped[str]
    last_name: Mapped[str]
    birthdate: Mapped[date]
