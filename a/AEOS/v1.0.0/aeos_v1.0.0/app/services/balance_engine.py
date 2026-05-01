from sqlalchemy.orm import Session
from app.models.ledger import LedgerEntry

def compute_balance(db: Session, entity_id: str, currency: str):
    entries = db.query(LedgerEntry).filter(
        LedgerEntry.entity_id == entity_id,
        LedgerEntry.currency == currency
    ).all()

    balance = 0.0

    for tx in entries:
        if tx.direction == "CREDIT":
            balance += tx.amount
        elif tx.direction == "DEBIT":
            balance -= tx.amount

    return balance
