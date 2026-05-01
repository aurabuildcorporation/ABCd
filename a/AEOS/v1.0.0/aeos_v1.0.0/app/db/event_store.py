import sqlite3
import time
from typing import Dict, Any, List

DB_PATH = "aeos_events.db"


def init_event_store():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS aic_events (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        entity TEXT NOT NULL,
        event_type TEXT NOT NULL,
        score REAL,
        grade TEXT,
        tier TEXT,
        credit_limit REAL,
        raw JSON,
        timestamp INTEGER
    )
    """)

    conn.commit()
    conn.close()


def append_event(event: Dict[str, Any]):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""
        INSERT INTO aic_events (
            entity, event_type, score, grade, tier, credit_limit, raw, timestamp
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        event.get("entity"),
        event.get("event_type", "AIC_SCORE_UPDATED"),
        event.get("score"),
        event.get("grade"),
        event.get("tier"),
        event.get("credit_limit"),
        str(event),
        int(time.time())
    ))

    conn.commit()
    conn.close()


def fetch_events(entity: str = None) -> List[dict]:
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    if entity:
        c.execute("SELECT * FROM aic_events WHERE entity = ?", (entity,))
    else:
        c.execute("SELECT * FROM aic_events")

    rows = c.fetchall()
    conn.close()

    return rows
