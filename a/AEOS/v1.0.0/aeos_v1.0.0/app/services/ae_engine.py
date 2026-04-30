
from app.services.ledger_engine import append_tx

def settle(entity_id, amount):
    # settlement currency only
    return append_tx(
        entity_id=entity_id,
        currency="AE",
        amount=amount,
        direction="DEBIT"
    )
