import sqlite3
from pathlib import Path

DB_PATH = Path("aeos.db")

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS aic_events (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        entity TEXT,
        event_type TEXT,
        payload TEXT,
        timestamp INTEGER
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS credit_decisions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        entity TEXT,
        score REAL,
        tier TEXT,
        credit_limit REAL,
        timestamp INTEGER
    )
    """)

    conn.commit()
    conn.close()
