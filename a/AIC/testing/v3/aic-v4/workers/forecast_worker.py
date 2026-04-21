import logging
from workers.utils.db_access import fetch_recent_scores

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("workers")

def forecast(entity):
    rows = fetch_recent_scores(entity, limit=30)
    if not rows:
        return None

    # Simple naive forecast: repeat last score
    last_score = rows[0]["score"]

    prediction = {
        "entity": entity,
        "forecast_score": last_score,
        "method": "naive"
    }

    logger.info(f"Forecast for {entity}: {prediction}")
    return prediction