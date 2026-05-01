from app.core.state import ENTITY_STATE
from app.domain.credit_policy import compute_credit_limit, determine_risk_tier


def build_state(entity: str, score: float, event: dict):

    tier = determine_risk_tier(score)
    credit_limit = compute_credit_limit(score)

    ENTITY_STATE[entity] = {
        "score": score,
        "tier": tier,
        "credit_limit": credit_limit,
        "last_event": event
    }

    return ENTITY_STATE[entity]
