from app.services.reducer import build_state
from app.ws.manager import manager


async def handle_aic_event(event: dict):

    entity = event["entity"]
    score = float(event.get("score", 0))

    state = build_state(entity, score, event)

    print(f"[AIC EVENT] {entity} → {state['tier']} → Limit {state['credit_limit']}")

    # 🔥 THIS WAS MISSING (the reason UI didn't update)
    await manager.broadcast({
        "type": "STATE_SNAPSHOT",
        "data": state
    })

    return state
