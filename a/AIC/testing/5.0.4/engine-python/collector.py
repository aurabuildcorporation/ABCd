from collectors.wikipedia import get_wikipedia_signals
from collectors.reddit import get_reddit_signals
from collectors.news import get_news_signals

def collect_all_signals(entity):

    wiki = get_wikipedia_signals(entity)
    reddit = get_reddit_signals(entity)
    news = get_news_signals(entity)

    return {
        "authority": wiki.get("authority", 20),
        "base": 120,  # can later become learned dataset
        "sentiment": reddit.get("sentiment", 0),
        "popularity": reddit.get("popularity", 20),
        "momentum": news.get("momentum", 10),
        "trust": news.get("trust", 30)
    }
