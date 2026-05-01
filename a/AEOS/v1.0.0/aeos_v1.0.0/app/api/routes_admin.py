from fastapi import APIRouter
import asyncio
from app.ws.manager import manager
from app.core.reducer import get_current_state
from app.db.sqlite import get_db
from fastapi import WebSocket, WebSocketDisconnect

router = APIRouter()

# ---------------------------
# HTTP: Current State
# ---------------------------

@router.get("/admin/state")
def admin_state(entity: str = None):
    return get_current_state(entity)


# ---------------------------
# HTTP: Recent Events
# ---------------------------

@router.get("/admin/events")
def admin_events():
    conn = get_db()
    cur = conn.cursor()

    cur.execute("SELECT * FROM aic_events ORDER BY id DESC LIMIT 100")
    rows = cur.fetchall()

    return [dict(r) for r in rows]


# ---------------------------
# WebSocket: Live Stream 
# ---------------------------

@router.websocket("/ws/admin")
async def admin_ws(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()  # keep alive only
    except:
        manager.disconnect(websocket)
