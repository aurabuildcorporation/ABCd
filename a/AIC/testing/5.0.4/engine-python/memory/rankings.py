import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "../database/aic_memory.db")


def get_conn():
    return sqlite3.connect(DB_PATH)


def latest_scores():
    conn = get_conn()
    c = conn.cursor()

    c.execute("""
        SELECT entity, MAX(created_at), score
        FROM entity_scores
        GROUP BY entity
        ORDER BY score DESC
    """)

    rows = c.fetchall()
    conn.close()

    return [{"entity": r[0], "score": r[2]} for r in rows]


def leaderboard(limit=10):
    data = latest_scores()
    return data[:limit]


def get_entity_score(entity):
    conn = get_conn()
    c = conn.cursor()

    c.execute("""
        SELECT score
        FROM entity_scores
        WHERE entity = ?
        ORDER BY created_at DESC
        LIMIT 1
    """, (entity,))

    row = c.fetchone()
    conn.close()

    return row[0] if row else None


def percentile(entity):
    data = latest_scores()

    scores = sorted([x["score"] for x in data])

    val = get_entity_score(entity)

    if val is None:
        return None

    below = sum(1 for s in scores if s <= val)

    pct = round((below / len(scores)) * 100, 2)

    return pct


def compare(a, b):
    sa = get_entity_score(a)
    sb = get_entity_score(b)

    if sa is None or sb is None:
        return None

    winner = a if sa > sb else b

    return {
        "entity1": a,
        "score1": sa,
        "entity2": b,
        "score2": sb,
        "winner": winner,
        "delta": round(abs(sa - sb), 2)
    }


def top_movers(limit=5):
    conn = get_conn()
    c = conn.cursor()

    c.execute("""
        SELECT entity, MIN(score), MAX(score)
        FROM entity_scores
        GROUP BY entity
    """)

    rows = c.fetchall()
    conn.close()

    movers = []

    for r in rows:
        delta = r[2] - r[1]
        movers.append({
            "entity": r[0],
            "change": round(delta, 2)
        })

    movers.sort(key=lambda x: x["change"], reverse=True)

    return movers[:limit]
