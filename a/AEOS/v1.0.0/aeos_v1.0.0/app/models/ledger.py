from sqlalchemy import Column, String, Float
from app.db.database import Base

class LedgerEntry(Base):
    __tablename__ = "ledger"

    id = Column(String, primary_key=True, index=True)
    entity_id = Column(String)
    currency = Column(String)  # PI or AE
    amount = Column(Float)
    direction = Column(String)
    timestamp = Column(Float)
    prev_hash = Column(String)
    hash = Column(String)
