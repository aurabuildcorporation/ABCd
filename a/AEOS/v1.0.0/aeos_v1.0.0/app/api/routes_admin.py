# app/api/routes_admin.py

from fastapi import APIRouter, WebSocket
import asyncio

from app.ws.manager import manager
from app.core.state import ENTITY_STATE
from app.core.reducer import get_current_state
from app.db.sqlite import get_db

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
            # FIX: no build_state() call here anymore
            state_snapshot = {
                "type": "STATE_SNAPSHOT",
                "data": ENTITY_STATE
            }

            await manager.broadcast(state_snapshot)

            await asyncio.sleep(1)

    except Exception as e:
        print("WS error:", e)
        manager.disconnect(websocket)
