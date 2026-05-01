import requests
import subprocess
import json

AIC_API = "http://127.0.0.1:5000/score"

def fetch_aic_score(entity_id: str):
    """
    Returns structured AIC response OR null-state if unavailable
    """

    # 1. Try API
    try:
        response = requests.post(AIC_API, json={"entity": entity_id}, timeout=2)

        if response.status_code == 200:
            return {
                "status": "available",
                "data": response.json()
            }

    except Exception:
        pass

    # 2. Try CLI fallback
    try:
        result = subprocess.run(
            ["aic", "score", entity_id],
            capture_output=True,
            text=True
        )

        return {
            "status": "available",
            "data": json.loads(result.stdout)
        }

    except Exception:
        # 3. HARD FAILURE STATE (IMPORTANT)
        return {
            "status": "unavailable",
            "data": None
        }
