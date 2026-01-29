from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from sqlalchemy.orm import selectinload
from app.models import Lot, LotStatus
from app.repositories.base_repository import BaseRepository


class LotRepository(BaseRepository[Lot]):
    def __init__(self, db: AsyncSession):
        super().__init__(db, Lot)

    async def get(self, lot_id: int) -> Optional[Lot]:
        query = select(self.model).options(selectinload(self.model.bids)).where(self.model.id == lot_id)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def get_all(self, status: Optional[LotStatus] = LotStatus.RUNNING,
                      skip: int = 0, limit: int = 100) -> List[Lot]:
        query = select(Lot).options(selectinload(Lot.bids))
        if status:
            query = query.where(self.model.status == status)
        query = query.order_by(Lot.created_at.desc()).offset(skip).limit(limit)
        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def create(self, **kwargs) -> Lot:
        instance = self.model(**kwargs)
        self.db.add(instance)
        await self.db.commit()
        await self.db.refresh(instance)
        lot_id = instance.id
        query = select(self.model).options(selectinload(self.model.bids)).where(self.model.id == lot_id)
        result = await self.db.execute(query)
        return result.scalar_one()

    async def update_lot_price(self, lot_id: int, new_price: float) -> Optional[Lot]:
        await self.db.execute(
            update(self.model)
            .where(self.model.id == lot_id)
            .values(current_price=new_price)
        )
        await self.db.commit()
        return await self.get(lot_id)
