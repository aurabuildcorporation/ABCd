from sqlalchemy import Column, String, Float
from app.db.database import Base
import uuid
import time


class CreditDecision(Base):
    __tablename__ = "credit_decisions"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    entity_id = Column(String)

    credit_limit = Column(Float)

    aic_score = Column(Float, nullable=True)
    aic_grade = Column(String, nullable=True)

    risk_tier = Column(String)
    source = Column(String)  # EVENT / API / FALLBACK

    timestamp = Column(Float, default=lambda: time.time())
