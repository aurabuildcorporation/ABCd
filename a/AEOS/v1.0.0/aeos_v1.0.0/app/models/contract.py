from sqlalchemy import Column, String
from app.db.database import Base

class Contract(Base):
    __tablename__ = "contracts"

    id = Column(String, primary_key=True, index=True)
    entity_id = Column(String)
    hash = Column(String)
    status = Column(String)
