# app/core/reducer.py
from app.db.event_store import get_events
from app.core.state import ENTITY_STATE

def build_state(entity, score, event):

    tier = determine_tier(score)
    credit_limit = map_credit(tier)

    ENTITY_STATE[entity] = {
        "score": score,
        "tier": tier,
        "credit_limit": credit_limit,
        "last_event": event
    }

    return ENTITY_STATE[entity]

def reduce_events(events):
    state = {}

    for e in events:
        entity = e["entity"]

        if entity not in state:
            state[entity] = {
                "score": 0,
                "tier": "T0",
                "credit_limit": 0,
                "last_event": None
            }

        if e["event"] == "AIC_SCORE_UPDATED":
            score = float(e.get("score", 0))

            state[entity]["score"] = score
            state[entity]["last_event"] = e

            # simple tier logic
            if score <= 300:
                state[entity]["tier"] = "T3"
            elif score <= 500:
                state[entity]["tier"] = "T2"
            else:
                state[entity]["tier"] = "T1"

    return state


def get_current_state(entity: str = None):
    events = get_events(entity)
    return reduce_events(events)
