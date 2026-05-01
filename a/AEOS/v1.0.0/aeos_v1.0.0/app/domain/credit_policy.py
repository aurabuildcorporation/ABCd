def compute_credit_limit(score: float) -> float:

    if score <= 300:
        return 0
    elif score <= 500:
        return 100
    elif score <= 750:
        return 1000
    else:
        return 10000


def determine_risk_tier(score: float) -> str:

    if score <= 300:
        return "T3"
    elif score <= 500:
        return "T2"
    elif score <= 750:
        return "T1"
    else:
        return "T0"
