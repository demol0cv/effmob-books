from pydantic import Field
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from typing import List, Optional, Sequence
from sqlalchemy.orm import joinedload
from core.models.base import Base
from core.schemas.base import ItemBase

class CRUDBase:
    def __init__(self, model:Base):
        self.model = model

    async def get_one_item(
            self,
            session: AsyncSession,
            id: int,
    ) -> Base | None:
        query = select(self.model).where(self.model.id == id)

        result = await session.execute(query)

        item = result.scalar_one_or_none()
        return item
    

    async def get_all_items(
            self,
            session: AsyncSession,
            page: int = 0,
            per_page: int = 15,
    ) -> Sequence[Base]:
        offset = page*per_page
        query = select(self.model).order_by(self.model.id).offset(offset).limit(per_page)
        result = await session.scalars(query)
        return result.all()
    
    async def create_item(
            self,
            session: AsyncSession,
            item_create: ItemBase,
    ) -> Base:
        item = ItemBase(**item_create.model_dump())
        session.add(item)
        await session.commit()
        return item
    
    async def remove_item(
            self,
            session: AsyncSession,
            id: int,
    ) -> Base:
        select_query = select(self.model).where(self.model.id == id)
        result = await session.execute(select_query)
        item = result.scalar_one_or_none()
        if item is not None:
            delete_query = delete(self.model).where(self.model.id == item.id)
            await session.execute(delete_query)
            await session.commit()
        
        return item
        
    