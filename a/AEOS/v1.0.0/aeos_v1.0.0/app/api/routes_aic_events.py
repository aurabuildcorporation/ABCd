from fastapi import APIRouter
from app.services.aic_event_handler import handle_aic_event

router = APIRouter()

@router.post("/aic/event")
async def aic_event(event: dict):
    state = await handle_aic_event(event)
    return {"status": "accepted", "state": state}
