import sqlite3
import os
from config.settings import DATABASE_PATH

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SCHEMA_FILE = os.path.join(BASE_DIR, "schema.sql")

def init_db():
    print(f"Initializing database at: {DATABASE_PATH}")

    conn = sqlite3.connect(DATABASE_PATH)
    cur = conn.cursor()

    with open(SCHEMA_FILE, "r") as f:
        schema_sql = f.read()
        cur.executescript(schema_sql)

    conn.commit()
    conn.close()
    print("Database initialized successfully.")

if __name__ == "__main__":
    init_db()