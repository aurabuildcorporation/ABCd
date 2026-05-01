def determine_risk_tier(score: float):
    if score is None:
        return "BLOCKED"

    if score <= 300:
        return "T3"
    elif score <= 500:
        return "T2"
    else:
        return "T1"
