
import os

FLASK_PORT = int(os.getenv("FLASK_PORT", "5000"))
NODE_ENGINE_URL = os.getenv("NODE_ENGINE_URL", "http://localhost:4000")
DATABASE_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "db", "aic.db")
