import math

# Unified weights (tunable later)
WEIGHTS = {
    "authority": 0.35,
    "sentiment": 0.25,
    "popularity": 0.15,
    "momentum": 0.15,
    "trust": 0.10
}

def normalize(x):
    """
    Log normalization prevents explosion and caps without hard limits
    """
    return math.log(1 + max(0, x))


def scale_to_1000(value, max_expected=10):
    """
    Converts normalized value into 0–1000 range
    """
    return 1000 * (value / (1 + max_expected))


def score_entity(entity, signals):

    # 1. normalize signals
    a = normalize(signals.get("authority", 0))
    s = normalize(signals.get("sentiment", 0))
    p = normalize(signals.get("popularity", 0))
    m = normalize(signals.get("momentum", 0))
    t = normalize(signals.get("trust", 0))

    # 2. weighted sum
    raw_score = (
        WEIGHTS["authority"] * a +
        WEIGHTS["sentiment"] * s +
        WEIGHTS["popularity"] * p +
        WEIGHTS["momentum"] * m +
        WEIGHTS["trust"] * t
    )

    # 3. scale to 0–1000
    final_score = scale_to_1000(raw_score)

    # 4. grade mapping
    if final_score >= 800:
        grade = "A"
    elif final_score >= 650:
        grade = "B"
    elif final_score >= 500:
        grade = "C"
    else:
        grade = "D"

    return {
        "entity": entity,
        "score": round(final_score, 2),
        "grade": grade,
        "signals": signals
    }
