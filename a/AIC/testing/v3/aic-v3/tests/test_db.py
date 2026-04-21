import unittest
import os
import sqlite3
from db.init_db import init_db
from config.settings import DATABASE_PATH

class TestDatabase(unittest.TestCase):

    def setUp(self):
        # Reset DB for testing
        if os.path.exists(DATABASE_PATH):
            os.remove(DATABASE_PATH)
        init_db()

    def test_db_created(self):
        self.assertTrue(os.path.exists(DATABASE_PATH))

    def test_tables_exist(self):
        conn = sqlite3.connect(DATABASE_PATH)
        cur = conn.cursor()

        cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = {row[0] for row in cur.fetchall()}

        expected = {"entities", "scores", "history", "logs"}
        self.assertTrue(expected.issubset(tables))

        conn.close()

if __name__ == "__main__":
    unittest.main()