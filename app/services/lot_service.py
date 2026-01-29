from typing import List, Optional
from app.models.lot_model import Lot, LotStatus
from app.repositories.lot_repository import LotRepository
from app.schemas.lot_schema import LotCreate
from app.services.base_service import BaseService


class LotService(BaseService[Lot, LotRepository]):
    def __init__(self, repository: LotRepository):
        super().__init__(repository)

    async def create_lot(self, lot_data: LotCreate) -> Lot:
        data = lot_data.model_dump()
        data["current_price"] = data["start_price"]
        data["status"] = LotStatus.RUNNING

        return await self.repository.create(**data)

    async def get_lot(self, lot_id: int) -> Optional[Lot]:
        return await self.repository.get(lot_id)

    async def get_active_lots(self, skip: int = 0, limit: int = 100) -> List[Lot]:
        return await self.repository.get_all(
            status=LotStatus.RUNNING,
            skip=skip,
            limit=limit
        )
