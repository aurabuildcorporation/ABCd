import requests
from urllib.parse import quote

POS = {"good","great","bullish","growth","win","profit","strong"}
NEG = {"bad","crash","loss","fraud","lawsuit","weak"}

def get_reddit_signals(entity):
    try:
        url = f"https://www.reddit.com/search.json?q={quote(entity)}&limit=25"
        headers = {"User-agent": "AIC-SCORE-V17"}

        res = requests.get(url, headers=headers, timeout=5)
        data = res.json()

        posts = data["data"]["children"]

        mentions = len(posts)
        score = 0

        for p in posts:
            text = p["data"]["title"].lower()

            if any(w in text for w in POS):
                score += 2
            elif any(w in text for w in NEG):
                score -= 2
            else:
                score += 0.5

        sentiment = score * 5
        momentum = min(100, mentions * 3)

        return {
            "sentiment": round(sentiment, 2),
            "momentum": round(momentum, 2),
            "reddit_mentions": mentions
        }

    except:
        return {
            "sentiment": 0.0,
            "momentum": 5.0,
            "reddit_mentions": 0
        }
