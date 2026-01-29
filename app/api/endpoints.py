from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from app import schemas
from app import services
from app.dependencies import get_lot_service, get_bid_service

router = APIRouter()


@router.post("/lots", response_model=schemas.LotResponse, status_code=status.HTTP_201_CREATED)
async def create_lot(
        lot_data: schemas.LotCreate,
        service: services.LotService = Depends(get_lot_service)
):
    return await service.create_lot(lot_data)


@router.get("/lots", response_model=List[schemas.LotListResponse])
async def get_lots(skip: int = 0, limit: int = 100, service: services.LotService = Depends(get_lot_service)):
    return await service.get_active_lots(skip, limit)


@router.get("/lots/{lot_id}", response_model=schemas.LotResponse)
async def get_lot(lot_id: int, service: services.LotService = Depends(get_lot_service)):
    lot = await service.get_lot(lot_id)
    if not lot:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Lot with id {lot_id} not found"
        )
    return lot


@router.post("/lots/{lot_id}/bids", response_model=schemas.BidResponse, status_code=status.HTTP_201_CREATED)
async def create_bid(lot_id: int, bid_data: schemas.BidCreate, service: services.BidService = Depends(get_bid_service)):
    try:
        return await service.place_bid(lot_id, bid_data)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/lots/{lot_id}/bids", response_model=List[schemas.BidResponse])
async def get_bids(lot_id: int, service: services.BidService = Depends(get_bid_service)):
    try:
        return await service.get_bids(lot_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
