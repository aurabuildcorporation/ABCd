# app/db/event_store.py

EVENT_STORE = []


def append_event(event: dict):
    EVENT_STORE.append(event)
    return event


def get_events(entity: str = None):
    if entity:
        return [e for e in EVENT_STORE if e.get("entity") == entity]
    return EVENT_STORE
