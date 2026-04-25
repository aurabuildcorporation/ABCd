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
        score INTEGER,
        authority INTEGER,
        sentiment INTEGER,
        popularity INTEGER,
        momentum INTEGER,
        trust INTEGER,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()


def save_score(entity, result):

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""
        INSERT INTO entity_scores
        (entity, score, authority, sentiment, popularity, momentum, trust)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        entity,
        result["score"],
        result["signals"]["authority"],
        result["signals"]["sentiment"],
        result["signals"]["popularity"],
        result["signals"]["momentum"],
        result["signals"]["trust"]
    ))

    conn.commit()
    conn.close()
