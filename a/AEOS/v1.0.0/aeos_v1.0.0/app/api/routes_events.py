# app/api/routes_events.py
from fastapi import APIRouter
from app.services.event_store import append_event
from app.ws.manager import manager

router = APIRouter()


@router.post("/event")
async def ingest_event(event: dict):
    stored = append_event(event)

    await manager.broadcast({
        "type": "EVENT",
        "data": stored
    })

    return {"status": "accepted"}
