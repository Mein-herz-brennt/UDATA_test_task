from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.repositories.bid_repository import BidRepository
from app.repositories.lot_repository import LotRepository
from app.services.bid_service import BidService
from app.services.lot_service import LotService


async def get_lot_service(db: AsyncSession = Depends(get_db)) -> LotService:
    repo = LotRepository(db)
    return LotService(repo)


async def get_bid_service(db: AsyncSession = Depends(get_db)) -> BidService:
    lot_repo = LotRepository(db)
    bid_repo = BidRepository(db)
    return BidService(bid_repo, lot_repo)
