import asyncio
import json
from fastapi import APIRouter, WebSocket, WebSocketDisconnect

router = APIRouter()

class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            await connection.send_json(message)

# Instantiate the manager so it can be imported
manager = ConnectionManager()

@router.websocket("/ws/admin")
async def admin_ws(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            # Keep connection alive and handle messages if needed
            data = await websocket.receive_text()
            # Example: echo back or process data
            # await manager.send_personal_message(f"You wrote: {data}", websocket)
            await asyncio.sleep(0.1) 
    except WebSocketDisconnect:
        manager.disconnect(websocket)
