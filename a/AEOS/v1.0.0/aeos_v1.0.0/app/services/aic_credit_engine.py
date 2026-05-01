# app/services/aic_credit_engine.py

def get_credit_limit(score: float):
    if score <= 300:
        return 0
    elif score <= 500:
        return 100
    elif score <= 750:
        return 1000
    return 10000
