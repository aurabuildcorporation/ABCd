
CREATE TABLE IF NOT EXISTS scores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    entity_name TEXT,
    aic_score REAL,
    confidence REAL,
    rating TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);
