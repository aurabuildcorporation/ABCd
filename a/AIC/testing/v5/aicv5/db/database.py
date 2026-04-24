import os, sqlite3
DB=os.getenv("SQLITE_PATH","db/aic.db")
def init_db():
    os.makedirs("db", exist_ok=True)
    con=sqlite3.connect(DB)
    con.execute("CREATE TABLE IF NOT EXISTS scores(id INTEGER PRIMARY KEY, entity TEXT, aic_score INTEGER, confidence REAL, ts DATETIME DEFAULT CURRENT_TIMESTAMP)")
    con.commit(); con.close()
def save_score(d):
    con=sqlite3.connect(DB)
    con.execute("INSERT INTO scores(entity,aic_score,confidence) VALUES(?,?,?)",(d.get("entity"), d.get("aic_score"), d.get("confidence",0)))
    con.commit(); con.close()
