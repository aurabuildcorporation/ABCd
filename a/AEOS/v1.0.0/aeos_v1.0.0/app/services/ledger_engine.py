
from app.services.hash_utils import make_hash
import time

LEDGER = []

def append_tx(entity_id, currency, amount, direction, prev_hash="GENESIS"):
    tx = {
        "entity_id": entity_id,
        "currency": currency,  # PI or AE
        "amount": amount,
        "direction": direction,
        "timestamp": time.time(),
        "prev_hash": prev_hash,
    }

    tx_str = str(tx)
    tx["hash"] = make_hash(tx_str + prev_hash)

    LEDGER.append(tx)
    return tx

def get_ledger():
    return LEDGER
