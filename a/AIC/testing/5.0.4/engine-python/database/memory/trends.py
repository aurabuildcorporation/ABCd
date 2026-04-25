import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "../database/aic_memory.db")

def get_entity_history(entity, limit=10):

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""
        SELECT score, created_at
        FROM entity_scores
        WHERE entity = ?
        ORDER BY created_at DESC
        LIMIT ?
    """, (entity, limit))

    rows = c.fetchall()
    conn.close()

    return rows


def calculate_trend(entity):

    history = get_entity_history(entity, 7)

    if len(history) < 2:
        return {
            "trend": "stable",
            "change": 0
        }

    latest = history[0][0]
    oldest = history[-1][0]

    change = latest - oldest

    if change > 30:
        trend = "rising"
    elif change < -30:
        trend = "declining"
    else:
        trend = "stable"

    return {
        "trend": trend,
        "change": change
    }
