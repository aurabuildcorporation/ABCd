import math

def clamp(value, min_v, max_v):
    return max(min_v, min(max_v, value))

def score_entity(entity, signals):

    authority = clamp(signals["authority"], 0, 200)
    base = clamp(signals["base"], 0, 200)

    sentiment = clamp(signals["sentiment"], -100, 150)
    sentiment_normalized = (sentiment + 100) * 0.6  # 0–150 scale

    popularity = clamp(signals["popularity"], 0, 150)
    momentum = clamp(signals["momentum"], 0, 150)
    trust = clamp(signals["trust"], 0, 150)

    total = (
        authority +
        base +
        sentiment_normalized +
        popularity +
        momentum +
        trust
    )

    score = round(clamp(total, 0, 1000), 2)

    return {
        "entity": entity,
        "score": score,
        "grade": grade(score),
        "signals": {
            "authority": authority,
            "base": base,
            "sentiment": sentiment_normalized,
            "popularity": popularity,
            "momentum": momentum,
            "trust": trust
        }
    }


def grade(score):
    if score >= 950: return "S+"
    if score >= 900: return "S"
    if score >= 850: return "A+"
    if score >= 800: return "A"
    if score >= 700: return "B"
    if score >= 600: return "C"
    return "D"
