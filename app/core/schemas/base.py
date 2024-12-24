from datetime import datetime, date

from pydantic import BaseModel, Field
from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import TIMESTAMP


class ItemBase(BaseModel):
    id: int

class ListItemsBase(BaseModel):
    items_list: list[ItemBase]
    page: int
    per_page: int

    @property
    def count(self) -> int:
        return len(self.items_list)
