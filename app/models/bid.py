from app.models.base import Base
from datetime import datetime
from sqlalchemy import Integer, String, Float, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship, Mapped, mapped_column


class Bid(Base):
    __tablename__ = "bids"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    lot_id: Mapped[int] = mapped_column(Integer, ForeignKey("lots.id", ondelete="CASCADE"), nullable=False, index=True)
    bidder_name: Mapped[str] = mapped_column(String(255), nullable=False)
    amount: Mapped[float] = mapped_column(Float, nullable=False)
    timestamp: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False, index=True)

    lot: Mapped["Lot"] = relationship("Lot", back_populates="bids")

