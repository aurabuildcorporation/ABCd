import sqlite3
from config.settings import DATABASE_PATH

def connect():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def get_entities():
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM entities")
    rows = cur.fetchall()
    conn.close()
    return rows

def save_score(entity_name, score, confidence):
    conn = connect()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO scores (entity_name, score, confidence, timestamp) VALUES (?, ?, ?, datetime('now'))",
        (entity_name, score, confidence)
    )
    conn.commit()
    conn.close()

def fetch_recent_scores(entity_name, limit=10):
    conn = connect()
    cur = conn.cursor()
    cur.execute(
        "SELECT score, confidence, timestamp FROM scores WHERE entity_name = ? ORDER BY timestamp DESC LIMIT ?",
        (entity_name, limit)
    )
    rows = cur.fetchall()
    conn.close()
    return rows