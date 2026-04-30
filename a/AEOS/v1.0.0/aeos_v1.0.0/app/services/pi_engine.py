
def calculate_pi_credit(aic_score: float, base_capital: float):
    # strict mode: capped exposure
    multiplier = min((aic_score / 1000) ** 1.5 * 3.0, 2.5)
    credit_line = base_capital * multiplier
    return credit_line, multiplier
