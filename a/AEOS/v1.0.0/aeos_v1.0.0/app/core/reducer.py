from typing import Dict, Any, List
from app.db.event_store import fetch_events


def reduce_entity_state(events: List[tuple]) -> Dict[str, Any]:
    state = {}

    for row in events:
        (
            _id,
            entity,
            event_type,
            score,
            grade,
            tier,
            credit_limit,
            raw,
            timestamp
        ) = row

        state[entity] = {
            "score": score,
            "grade": grade,
            "tier": tier,
            "credit_limit": credit_limit,
            "last_updated": timestamp
        }

    return state


def get_current_state(entity: str = None):
    events = fetch_events(entity)
    return reduce_entity_state(events)	
