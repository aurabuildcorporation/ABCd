from app.services.aic_client import fetch_aic_score


def validate_transaction(entity_id: str, amount: float):
    """
    Validates whether an entity is allowed to perform a transaction.
    Returns (bool, reason)
    """

    result = fetch_aic_score(entity_id)

    # =========================
    # AIC UNAVAILABLE → BLOCK
    # =========================
    if result["status"] != "available":
        return False, "AIC_UNAVAILABLE - TRANSACTION_BLOCKED"

    data = result["data"]
    score = data.get("score", 0)

    # =========================
    # RISK POLICY
    # =========================
    if score < 300:
        return False, "LOW_SCORE - TRANSACTION_BLOCKED"

    if score < 500 and amount > 100:
        return False, "LIMIT_EXCEEDED_T2"

    if score < 750 and amount > 1000:
        return False, "LIMIT_EXCEEDED_T3"

    # =========================
    # PASS
    # =========================
    return True, "APPROVED"
