DROP TABLE IF EXISTS scores;

CREATE TABLE scores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    entity_name TEXT NOT NULL,
    aic_score INTEGER NOT NULL,
    rating TEXT NOT NULL,
    semantic_intelligence REAL,
    cultural_momentum REAL,
    external_credibility REAL,
    sentiment_stability REAL,
    system_confidence REAL,
    confidence REAL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);
