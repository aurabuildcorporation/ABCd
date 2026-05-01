from app.db.database import Base, engine
from app.models import credit_decision

# import ALL models so SQLAlchemy registers them
from app.models import entity, ledger, contract

def init_db():
    Base.metadata.create_all(bind=engine)
