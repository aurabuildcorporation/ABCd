from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.services.balance_engine import compute_balance

router = APIRouter(prefix="/balance")

@router.get("/")
def get_balance(entity_id: str, currency: str, db: Session = Depends(get_db)):
    return {
        "entity_id": entity_id,
        "currency": currency,
        "balance": compute_balance(db, entity_id, currency)
    }
