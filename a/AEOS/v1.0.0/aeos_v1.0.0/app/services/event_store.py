# app/services/event_store.py
EVENT_STORE = []


def append_event(event: dict):
    EVENT_STORE.append(event)
    return event


def get_events(limit: int = 100):
    return EVENT_STORE[-limit:]

import json
from app.db.sqlite import get_db

def append_event(entity: str, event_type: str, payload: dict, timestamp: int):
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO aic_events (entity, event_type, payload, timestamp)
        VALUES (?, ?, ?, ?)
    """, (entity, event_type, json.dumps(payload), timestamp))

    conn.commit()
    conn.close()
