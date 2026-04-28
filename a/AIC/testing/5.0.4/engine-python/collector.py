from collectors.wiki import get_wikipedia_signals
from collectors.news import get_news_signals
from collectors.reddit import get_reddit_signals

def collect_all_signals(entity):

    wiki = get_wikipedia_signals(entity)
    news = get_news_signals(entity)
    reddit = get_reddit_signals(entity)

    return {
        "authority": wiki["authority"],
        "sentiment": reddit["sentiment"],
        "popularity": news["popularity"],
        "momentum": reddit["momentum"],
        "trust": news["trust"]
    }
