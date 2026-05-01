from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.services.ledger_engine import get_ledger

router = APIRouter(prefix="/ledger")

@router.get("/")
def ledger(db: Session = Depends(get_db)):
    return get_ledger(db)
