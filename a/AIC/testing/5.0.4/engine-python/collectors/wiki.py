import requests
import math
from urllib.parse import quote

def get_wikipedia_signals(entity):
    try:
        url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{quote(entity)}"
        res = requests.get(url, timeout=5)
        data = res.json()

        extract = data.get("extract", "")
        title = data.get("title")

        if not title:
            return {"authority": 5.0, "wiki_page": False}

        length = len(extract)
        authority = 20 + (math.log(1 + length) * 18)

        return {
            "authority": round(authority, 2),
            "wiki_page": True
        }

    except:
        return {
            "authority": 5.0,
            "wiki_page": False
        }
