import requests

def get_news_signals(entity):

    try:
        url = f"https://news.google.com/rss/search?q={entity}"
        res = requests.get(url, timeout=5)

        text = res.text.lower()

        mentions = text.count(entity.lower())

        # log-based normalization (prevents saturation)
        import math

        frequency_score = math.log(1 + mentions)

        return {
            "frequency": frequency_score,
            "raw_mentions": mentions,
            "source": "news",
            "trust_signal": 1 if mentions > 0 else 0
        }

    except:
        return {
            "frequency": 0,
            "raw_mentions": 0,
            "source": "news",
            "trust_signal": 0
        }
