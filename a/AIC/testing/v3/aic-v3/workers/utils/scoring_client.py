import requests
from config.settings import NODE_ENGINE_URL

def score_entity(entity_name):
    response = requests.post(
        f"{NODE_ENGINE_URL}/score",
        json={"entity": entity_name},
        timeout=10
    )
    response.raise_for_status()
    return response.json()