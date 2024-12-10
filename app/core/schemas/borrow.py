from datetime import datetime

from pydantic import BaseModel


class BorrowBase(BaseModel):
    book_id: int
    reader_name: str
    borrow_date: datetime
    return_date: datetime

class BorrowCreate(BorrowBase):
    pass

class BorrowRead(BorrowBase):
    id: int
