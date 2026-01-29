from typing import List
from app.services.base_service import BaseService
from app.repositories.bid_repository import BidRepository
from app.repositories.lot_repository import LotRepository
from app.models.bid_model import Bid
from app.models.lot_model import LotStatus
from app.schemas.bid_schema import BidCreate, WebSocketBidMessage
from app.websocket import manager


class BidService(BaseService[Bid, BidRepository]):
    def __init__(self, bid_repository: BidRepository, lot_repository: LotRepository):
        super().__init__(bid_repository)
        self.lot_repository = lot_repository

    async def place_bid(self, lot_id: int, bid_data: BidCreate) -> Bid:
        lot = await self.lot_repository.get(lot_id)
        if not lot:
            raise ValueError(f"Lot with id {lot_id} not found")

        if lot.status != LotStatus.RUNNING:
            raise ValueError(f"Lot with id {lot_id} is not active")

        if bid_data.amount <= lot.current_price:
            raise ValueError(f"Bid amount must be higher than current price {lot.current_price}")

        new_bid = await self.repository.create(lot_id=lot_id, **bid_data.model_dump())
        await self.lot_repository.update_lot_price(lot_id, bid_data.amount)
        message = WebSocketBidMessage(
            type="bid_placed",
            lot_id=lot_id,
            bidder=bid_data.bidder_name,
            amount=bid_data.amount
        )
        await manager.broadcast_bid(lot_id, message.model_dump())

        return new_bid

    async def get_bids(self, lot_id: int) -> List[Bid]:
        lot = await self.lot_repository.get(lot_id)
        if not lot:
            raise ValueError(f"Lot with id {lot_id} not found")

        return await self.repository.get_bids_by_lot(lot_id)
