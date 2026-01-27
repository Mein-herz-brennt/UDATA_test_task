from typing import Optional, List
from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.base import BaseRepository
from app.models.bid import Bid


class BidRepository(BaseRepository[Bid]):
    def __init__(self, db: AsyncSession):
        super().__init__(db, Bid)

    async def get_highest_bid(self, lot_id: int) -> Optional[Bid]:
        query = (
            select(self.model)
            .where(self.model.lot_id == lot_id)
            .order_by(desc(self.model.amount))
            .limit(1)
        )
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def get_bids_by_lot(self, lot_id: int) -> List[Bid]:
        query = (
            select(self.model)
            .where(self.model.lot_id == lot_id)
            .order_by(desc(self.model.timestamp))
        )
        result = await self.db.execute(query)
        return list(result.scalars().all())
