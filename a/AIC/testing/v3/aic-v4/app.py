from flask import Flask, render_template, request, jsonify
import requests
import sqlite3
import os
from config.settings import FLASK_PORT, NODE_ENGINE_URL, DATABASE_PATH

app = Flask(__name__, template_folder="frontend/templates", static_folder="frontend/static")


def get_db():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/entity/<entity_id>")
def entity_page(entity_id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM entities WHERE id = ?", (entity_id,))
    entity = cur.fetchone()

    cur.execute("SELECT * FROM scores WHERE entity_id = ? ORDER BY timestamp DESC LIMIT 50", (entity_id,))
    history = cur.fetchall()

    return render_template("entity.html", entity=entity, history=history)


@app.route("/api/score", methods=["POST"])
def score_entity():
    data = request.json
    entity_name = data.get("entity")

    if not entity_name:
        return jsonify({"error": "Missing entity"}), 400

    try:
        response = requests.post(f"{NODE_ENGINE_URL}/score", json={"entity": entity_name})
        result = response.json()
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO scores (entity_name, score, confidence, timestamp) VALUES (?, ?, ?, datetime('now'))",
        (entity_name, result["score"], result["confidence"])
    )
    conn.commit()

    return jsonify(result)


@app.route("/history/<entity>")
def history(entity):
    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        "SELECT score, confidence, timestamp FROM scores WHERE entity_name = ? ORDER BY timestamp ASC",
        (entity,)
    )
    rows = cur.fetchall()
    return render_template("history.html", entity=entity, history=rows)


@app.route("/admin")
def admin():
    return render_template("admin.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=FLASK_PORT, debug=True)