import requests

POSITIVE = {"good", "great", "bullish", "growth", "win", "profit", "success"}
NEGATIVE = {"bad", "crash", "loss", "hack", "lawsuit", "decline", "fraud"}

def get_reddit_signals(entity):

    try:
        url = f"https://www.reddit.com/search.json?q={entity}&limit=25"
        headers = {"User-agent": "AIC-SCORE-V2"}

        res = requests.get(url, headers=headers, timeout=5)
        data = res.json()

        posts = data["data"]["children"]

        sentiment_score = 0
        relevance_score = 0

        for p in posts:
            text = p["data"]["title"].lower()
            relevance_score += 1  # every mention counts lightly

            if any(w in text for w in POSITIVE):
                sentiment_score += 2
            elif any(w in text for w in NEGATIVE):
                sentiment_score -= 2
            else:
                sentiment_score += 0.5

        # normalize internally (NO HARD CAPS)
        return {
            "sentiment": sentiment_score,
            "relevance": relevance_score,
            "source": "reddit",
            "confidence": min(1.0, relevance_score / 25)
        }

    except:
        return {
            "sentiment": 0,
            "relevance": 0,
            "source": "reddit",
            "confidence": 0.1
        }
