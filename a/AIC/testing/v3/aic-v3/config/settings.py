import os

# Flask server port
FLASK_PORT = int(os.getenv("FLASK_PORT", 5000))

# Node scoring engine URL
NODE_ENGINE_HOST = os.getenv("NODE_ENGINE_HOST", "127.0.0.1")
NODE_ENGINE_PORT = int(os.getenv("NODE_ENGINE_PORT", 7000))
NODE_ENGINE_URL = f"http://{NODE_ENGINE_HOST}:{NODE_ENGINE_PORT}"

# SQLite database path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATABASE_PATH = os.path.join(BASE_DIR, "db", "aic.db")

# Logging configuration file
LOGGING_CONFIG = os.path.join(BASE_DIR, "config", "logging.conf")

# Yelp API keys
YELP_API_KEY = os.getenv("YELP_API_KEY", "")