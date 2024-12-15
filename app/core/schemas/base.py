from datetime import datetime, date

from pydantic import BaseModel, Field
from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import TIMESTAMP


class ItemBase(BaseModel):
    pass
