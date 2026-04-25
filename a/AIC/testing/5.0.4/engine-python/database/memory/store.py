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


def save_score(entity, score_data):

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""
        INSERT INTO entity_scores
        (entity, score, authority, sentiment, popularity, momentum, trust)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        entity,
        score_data["score"],
        score_data["signals"]["authority"],
        score_data["signals"]["sentiment"],
        score_data["signals"]["popularity"],
        score_data["signals"]["momentum"],
        score_data["signals"]["trust"]
    ))

    conn.commit()
    conn.close()
