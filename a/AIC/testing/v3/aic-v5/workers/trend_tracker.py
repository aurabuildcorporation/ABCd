import logging
from workers.utils.db_access import fetch_recent_scores

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("workers")

def moving_average(values, window=5):
    if len(values) < window:
        return None
    return sum(values[:window]) / window

def compute_trend(entity):
    rows = fetch_recent_scores(entity, limit=20)
    if not rows:
        return None

    scores = [r["score"] for r in rows]

    short = moving_average(scores, window=5)
    long = moving_average(scores, window=15)

    if short is None or long is None:
        return None

    trend = "up" if short > long else "down"
    logger.info(f"Trend for {entity}: {trend}")

    return {"entity": entity, "trend": trend, "short": short, "long": long}