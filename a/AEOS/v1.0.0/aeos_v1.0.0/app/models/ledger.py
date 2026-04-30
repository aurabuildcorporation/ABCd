
from pydantic import BaseModel

class LedgerEntry(BaseModel):
    entity_id: str
    currency: str
    amount: float
    direction: str
