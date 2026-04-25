import requests
import math

def get_wikipedia_signals(entity):

    try:
        url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{entity}"
        res = requests.get(url, timeout=5)
        data = res.json()

        extract = data.get("extract", "")
        title = data.get("title", "")

        if not extract:
            return {
                "authority": 0,
                "has_page": False,
                "quality": 0
            }

        length = len(extract)
        words = len(extract.split())

        # log-scaled authority (prevents inflation)
        authority = math.log(1 + length) * math.log(1 + words)

        return {
            "authority": authority,
            "has_page": True,
            "quality": 1,
            "source": "wikipedia"
        }

    except:
        return {
            "authority": 0,
            "has_page": False,
            "quality": 0
        }
