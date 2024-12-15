from datetime import UTC, date, datetime
from typing import Optional

from faker import Faker
from pydantic import BaseModel, Field

fake = Faker()

class BorrowBase(BaseModel):
    book_id: int
    reader_name: str
    is_active: bool = Field(default=False)
    borrow_date: datetime = Field(readOnly=True)
    return_date: datetime | None = Field(default=None, readOnly=True)

class BorrowCreate(BorrowBase):
    reader_name: str  = Field(examples=[fake.name() for _ in range(15)])
    borrow_date: datetime = Field(default=datetime.now(tz=UTC), readOnly=True)
    return_date: datetime | None = Field(default=None, readOnly=True)

class BorrowRead(BorrowBase):
    id: int

class BorrowFinish(BorrowBase):
    return_date: datetime = Field(default=datetime.now(tz=UTC), readOnly=True)