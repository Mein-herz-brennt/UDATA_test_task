from datetime import datetime
from sqlalchemy import Integer, String, Float, DateTime, Enum as SQLEnum
from sqlalchemy.orm import relationship, Mapped, mapped_column
import enum
from app.models.base import Base


class LotStatus(str, enum.Enum):
    RUNNING = "running"
    ENDED = "ended"


class Lot(Base):
    __tablename__ = "lots"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(String(1000), nullable=True)
    start_price: Mapped[float] = mapped_column(Float, nullable=False)
    current_price: Mapped[float] = mapped_column(Float, nullable=False)
    status: Mapped[LotStatus] = mapped_column(
        SQLEnum(LotStatus),
        default=LotStatus.RUNNING,
        nullable=False
    )
    end_time: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    bids: Mapped[list["Bid"]] = relationship(
        "Bid",
        back_populates="lot",
        cascade="all, delete-orphan",
        order_by="Bid.timestamp.desc()"
    )
