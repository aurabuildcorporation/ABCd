from app.services.reducer import build_state
from app.ws.manager import manager

async def handle_aic_event(event: dict):

    entity = event["entity"]
    score = float(event.get("score", 0))

    state = build_state(entity, score, event)

    print(f"[AIC EVENT] {entity} → {state['tier']} → Limit {state['credit_limit']}")

    # 🔥 SEND CLEAN EVENT (NOT NESTED)
    await manager.broadcast({
        "type": "EVENT",
        "entity": entity,
        "score": state["score"],
        "tier": state["tier"],
        "credit_limit": state["credit_limit"],
        "timestamp": event.get("timestamp")
    })

    return state
