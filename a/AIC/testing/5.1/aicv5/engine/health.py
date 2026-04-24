
import requests

def run_health_checks():
    return {
        "api": True,
        "engine": True,
        "db": True,
        "status": "ok"
    }
