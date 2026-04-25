import requests

def get_reddit_signals(entity):

    try:
        url = f"https://www.reddit.com/search.json?q={entity}&limit=25"
        headers = {"User-agent": "AIC-SCORE"}

        res = requests.get(url, headers=headers)
        data = res.json()

        posts = data["data"]["children"]

        mentions = len(posts)

        positive = 0
        negative = 0

        for p in posts:
            text = p["data"]["title"].lower()

            if any(word in text for word in ["good", "great", "bullish", "win", "growth"]):
                positive += 1
            if any(word in text for word in ["bad", "crash", "loss", "hack", "lawsuit"]):
                negative += 1

        sentiment = (positive - negative)

        return {
            "popularity": min(150, mentions * 6),
            "sentiment": sentiment * 10,
            "momentum": min(150, mentions * 4)
        }

    except:
        return {
            "popularity": 20,
            "sentiment": 0,
            "momentum": 10
        }
