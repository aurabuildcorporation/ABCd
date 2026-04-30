
from fastapi import APIRouter
from app.services.ae_engine import settle

router = APIRouter(prefix="/ae")

@router.post("/settle")
def settle_tx(entity_id: str, amount: float):
    return settle(entity_id, amount)
