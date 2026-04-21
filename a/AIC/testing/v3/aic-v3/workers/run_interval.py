import time
import requests
from workers.utils.db_access import get_entities, save_score
from workers.utils.scoring_client import score_entity
from config.settings import NODE_ENGINE_URL
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("workers")

INTERVAL_SECONDS = 60  # run every minute

def run():
    logger.info("Starting interval scoring worker...")

    while True:
        entities = get_entities()

        for entity in entities:
            name = entity["name"]
            logger.info(f"Scoring entity: {name}")

            try:
                result = score_entity(name)
                save_score(name, result["score"], result["confidence"])
                logger.info(f"Saved score for {name}: {result}")
            except Exception as e:
                logger.error(f"Error scoring {name}: {e}")

        time.sleep(INTERVAL_SECONDS)

if __name__ == "__main__":
    run()