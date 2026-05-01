from fastapi import APIRouter
from app.services.aic_event_handler import handle_aic_event

router = APIRouter()

@router.post("/aic/event")
async def aic_event(event: dict):

    # Normalize event (prevent missing fields)
    normalized = {
        "event": event.get("event", "AIC_SCORE_UPDATED"),
        "entity": event.get("entity"),
        "score": float(event.get("score", 0)),
        "grade": event.get("grade", "N/A"),
        "trend": event.get("trend", "unknown"),
        "timestamp": event.get("timestamp")
    }

    state = await handle_aic_event(normalized)

    return {"status": "accepted", "state": state}
