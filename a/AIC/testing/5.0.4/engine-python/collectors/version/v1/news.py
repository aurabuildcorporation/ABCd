import requests

def get_news_signals(entity):

    try:
        url = f"https://news.google.com/rss/search?q={entity}"
        res = requests.get(url)

        count = res.text.lower().count(entity.lower())

        trust = min(150, count * 8)
        momentum = min(150, count * 5)

        return {
            "trust": trust,
            "momentum": momentum
        }

    except:
        return {
            "trust": 30,
            "momentum": 10
        }
