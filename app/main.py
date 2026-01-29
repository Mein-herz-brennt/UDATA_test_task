import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware

from app.database import engine
from app.models.base_model import Base
from app.api import api_router as api_router
from app.websocket import manager

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()


app = FastAPI(
    title="Auction Service API",
    description="Real-time auction service with WebSocket support",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api", tags=["auction"])


@app.get("/")
async def root():
    return {
        "status": "online",
        "message": "Auction Service API is running",
        "docs": "/docs"
    }


@app.websocket("/ws/lots/{lot_id}")
async def websocket_endpoint(websocket: WebSocket, lot_id: int):
    await manager.connect(websocket, lot_id)
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"Message received: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket, lot_id)
    except Exception as e:
        manager.disconnect(websocket, lot_id)
        logger.error(f"WebSocket error on lot {lot_id}: {e}")
