import sqlite3
from config.settings import DATABASE_PATH

def get_connection():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def insert_score(entity_name, score, confidence):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO scores (entity_name, score, confidence, timestamp) VALUES (?, ?, ?, datetime('now'))",
        (entity_name, score, confidence)
    )
    conn.commit()
    conn.close()

def fetch_scores(entity_name, limit=50):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT score, confidence, timestamp FROM scores WHERE entity_name = ? ORDER BY timestamp DESC LIMIT ?",
        (entity_name, limit)
    )
    rows = cur.fetchall()
    conn.close()
    return rows

def log(level, message):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO logs (level, message, timestamp) VALUES (?, ?, datetime('now'))",
        (level, message)
    )
    conn.commit()
    conn.close()