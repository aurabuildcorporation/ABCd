
from app.services.ledger_engine import append_tx

def credit_pi(entity_id, amount):
    return append_tx(entity_id, "PI", amount, "CREDIT")

def debit_pi(entity_id, amount):
    return append_tx(entity_id, "PI", amount, "DEBIT")
