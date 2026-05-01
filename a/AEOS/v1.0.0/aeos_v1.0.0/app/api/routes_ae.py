from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.services.ledger_engine import append_tx

router = APIRouter(prefix="/ae")

@router.post("/settle")
def settle(entity_id: str, amount: float, db: Session = Depends(get_db)):
    return append_tx(db, entity_id, "AE", amount, "DEBIT")
