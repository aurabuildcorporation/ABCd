import requests
import math
from urllib.parse import quote

def get_news_signals(entity):
    try:
        url = f"https://news.google.com/rss/search?q={quote(entity)}"
        res = requests.get(url, timeout=5)
        text = res.text.lower()

        mentions = text.count(entity.lower())

        popularity = 10 + (math.log(1 + mentions) * 12)
        trust = min(100, 25 + mentions)

        return {
            "popularity": round(popularity, 2),
            "trust": round(trust, 2),
            "news_mentions": mentions
        }

    except:
        return {
            "popularity": 8.0,
            "trust": 15.0,
            "news_mentions": 0
        }
