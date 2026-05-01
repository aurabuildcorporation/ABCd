from app.services.aic_client import fetch_aic_score
from app.services.risk_engine import determine_risk_tier
from app.services.credit_ledger import log_credit_decision
from app.core.state import ENTITY_STATE


def get_credit_limit(entity: str):
    entity_state = ENTITY_STATE.get(entity)

    if not entity_state:
        return 0

    score = entity_state.get("score", 0)

    if score <= 300:
        return 0
    elif score <= 500:
        return 100
    elif score <= 750:
        return 1000
    return 10000


def _map_tier_to_credit(tier: str) -> float:
    mapping = {
        "T0": 0,
        "T1": 0,
        "T2": 100,
        "T3": 1000,
        "T4": 10000
    }

    return mapping.get(tier, 0)
