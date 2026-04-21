import logging
from workers.utils.db_access import fetch_recent_scores

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("workers")

THRESHOLD = 0.25  # 25% jump/drop

def detect_anomalies(entity):
    scores = fetch_recent_scores(entity, limit=10)
    if len(scores) < 2:
        return None

    latest = scores[0]["score"]
    previous = scores[1]["score"]

    change = abs(latest - previous)

    if change >= THRESHOLD:
        logger.warning(f"ANOMALY DETECTED for {entity}: Δ={change:.3f}")
        return {"entity": entity, "change": change}

    return None