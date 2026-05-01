import time
import uuid
from sqlalchemy.orm import Session
from app.models.ledger import LedgerEntry
from app.services.hash_utils import make_hash
from app.services.validation_engine import validate_transaction

def get_last_hash(db: Session):
    last = db.query(LedgerEntry).order_by(LedgerEntry.timestamp.desc()).first()
    return last.hash if last else "GENESIS"

def append_tx(db: Session, entity_id, currency, amount, direction):

    # VALIDATION STEP (NEW)
    valid, msg = validate_transaction(db, entity_id, currency, amount, direction)

    if not valid:
        return {
            "status": "REJECTED",
            "reason": msg
        }

    prev_hash = get_last_hash(db)

    timestamp = time.time()
    tx_data = f"{entity_id}{currency}{amount}{direction}{timestamp}{prev_hash}"
    tx_hash = make_hash(tx_data)

    tx = LedgerEntry(
        id=str(uuid.uuid4()),
        entity_id=entity_id,
        currency=currency,
        amount=amount,
        direction=direction,
        timestamp=timestamp,
        prev_hash=prev_hash,
        hash=tx_hash
    )

    db.add(tx)
    db.commit()
    db.refresh(tx)

    return {
        "status": "ACCEPTED",
        "tx": tx
    }

def get_ledger(db: Session):
    return db.query(LedgerEntry).all()
