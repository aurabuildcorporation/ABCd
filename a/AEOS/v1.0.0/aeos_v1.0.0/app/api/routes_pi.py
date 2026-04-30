
from fastapi import APIRouter
from app.services.transaction_service import credit_pi, debit_pi

router = APIRouter(prefix="/pi")

@router.post("/credit")
def credit(entity_id: str, amount: float):
    return credit_pi(entity_id, amount)

@router.post("/debit")
def debit(entity_id: str, amount: float):
    return debit_pi(entity_id, amount)
