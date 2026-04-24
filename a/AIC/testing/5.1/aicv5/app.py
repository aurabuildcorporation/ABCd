
from flask import Flask, request, jsonify, render_template
import sqlite3
import requests
from config.settings import FLASK_PORT, NODE_ENGINE_URL, DATABASE_PATH
from engine.health import run_health_checks

app = Flask(__name__, template_folder="frontend/templates", static_folder="frontend/static")

def get_db():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/health")
def health():
    return jsonify(run_health_checks())

@app.route("/api/score", methods=["POST"])
def score():
    data = request.json or {}
    query = data.get("query", {})

    payload = {
        "entity": query.get("text"),
        "type": query.get("type", "brand"),
        "mode": query.get("mode", "deep")
    }

    try:
        r = requests.post(f"{NODE_ENGINE_URL}/score", json=payload, timeout=20)
        return jsonify(r.json())
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=FLASK_PORT, debug=True)
