from app.db.event_store import append_event
from app.core.reducer import get_current_state
from app.ws.manager import manager


async def handle_aic_event(event: dict):

    # 1. persist immutable event
    append_event(event)

    entity = event["entity"]

    # 2. compute new derived state
    state = get_current_state(entity)

    print(f"[AIC EVENT] {entity} → {state[entity]['tier']}")

    # 3. broadcast EVENT (not full snapshot)
    await manager.broadcast({
        "type": "AIC_EVENT",
        "event": event,
        "state": state[entity]
    })

    return state[entity]
