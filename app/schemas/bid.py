from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict


class BidBase(BaseModel):
    bidder_name: str = Field(..., min_length=1, max_length=255)
    amount: float = Field(..., gt=0)


class BidCreate(BidBase):
    pass


class BidResponse(BidBase):
    id: int
    lot_id: int
    timestamp: datetime
    model_config = ConfigDict(from_attributes=True)


class WebSocketBidMessage(BaseModel):
    type: str = "bid_placed"
    lot_id: int
    bidder: str
    amount: float
