from typing import Dict, List
from fastapi import WebSocket


class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[int, List[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, lot_id: int):
        await websocket.accept()
        if lot_id not in self.active_connections:
            self.active_connections[lot_id] = []
        self.active_connections[lot_id].append(websocket)

    def disconnect(self, websocket: WebSocket, lot_id: int):
        if lot_id in self.active_connections:
            try:
                self.active_connections[lot_id].remove(websocket)
                if not self.active_connections[lot_id]:
                    del self.active_connections[lot_id]
            except ValueError:
                pass

    async def broadcast_bid(self, lot_id: int, message: dict):
        if lot_id in self.active_connections:
            connections = self.active_connections[lot_id].copy()
            disconnected = []
            
            for connection in connections:
                try:
                    await connection.send_json(message)
                except Exception:
                    disconnected.append(connection)
            
            for connection in disconnected:
                self.disconnect(connection, lot_id)


manager = ConnectionManager()
