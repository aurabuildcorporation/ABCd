from app.models.credit_decision import CreditDecision


def log_credit_decision(
    db,
    entity_id,
    credit_limit,
    aic_score,
    aic_grade,
    risk_tier,
    source
):
    entry = CreditDecision(
        entity_id=entity_id,
        credit_limit=credit_limit,
        aic_score=aic_score,
        aic_grade=aic_grade,
        risk_tier=risk_tier,
        source=source
    )

    db.add(entry)
    db.commit()
