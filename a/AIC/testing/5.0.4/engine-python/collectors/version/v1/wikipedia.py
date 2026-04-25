import requests

def get_wikipedia_signals(entity):

    url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{entity}"

    try:
        res = requests.get(url)
        data = res.json()

        if "title" not in data:
            return {"authority": 20}

        desc_length = len(data.get("extract", ""))

        authority = min(200, 50 + (desc_length / 5))

        return {
            "authority": round(authority, 2),
            "has_page": True
        }

    except:
        return {"authority": 10, "has_page": False}
