from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.services.ledger_engine import append_tx

router = APIRouter(prefix="/pi")

@router.post("/credit")
def credit(entity_id: str, amount: float, db: Session = Depends(get_db)):
    return append_tx(db, entity_id, "PI", amount, "CREDIT")

@router.post("/debit")
def debit(entity_id: str, amount: float, db: Session = Depends(get_db)):
    return append_tx(db, entity_id, "PI", amount, "DEBIT")
