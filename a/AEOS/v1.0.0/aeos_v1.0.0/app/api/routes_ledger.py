
from fastapi import APIRouter
from app.services.ledger_engine import get_ledger

router = APIRouter(prefix="/ledger")

@router.get("/")
def ledger():
    return get_ledger()
