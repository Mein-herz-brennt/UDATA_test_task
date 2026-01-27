from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, ConfigDict
from app.schemas.bid import BidResponse


class LotBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=1000)
    start_price: float = Field(..., gt=0)
    end_time: Optional[datetime] = None


class LotCreate(LotBase):
    pass


class LotUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=1000)
    status: Optional[str] = None


class LotResponse(LotBase):
    id: int
    current_price: float
    status: str
    created_at: datetime
    bids: List[BidResponse] = []
    model_config = ConfigDict(from_attributes=True)


class LotListResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    start_price: float
    current_price: float
    status: str
    end_time: Optional[datetime]
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)
