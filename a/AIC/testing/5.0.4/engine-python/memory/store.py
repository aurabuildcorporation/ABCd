import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "../database/aic_memory.db")


def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS entity_scores (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        entity TEXT,
        score REAL,
        authority REAL,
        sentiment REAL,
        popularity REAL,
        momentum REAL,
        trust REAL,
        model_version TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()


def save_score(entity, result):

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    signals = result["signals"]

    c.execute("""
        INSERT INTO entity_scores
        (entity, score, authority, sentiment, popularity, momentum, trust, model_version)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        entity,
        result["score"],
        signals.get("authority", 0),
        signals.get("sentiment", 0),
        signals.get("popularity", 0),
        signals.get("momentum", 0),
        signals.get("trust", 0),
        "v1.6"
    ))

    conn.commit()
    conn.close()
