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

def classify_aic(score: int) -> str:
    if score >= 900:
        return "Transcendent"
    elif score >= 800:
        return "Elite"
    elif score >= 700:
        return "Excellent"
    elif score >= 600:
        return "Competent"
    elif score >= 400:
        return "Developing"
    else:
        return "Unstable"


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

    normalized = result.get("normalized_score", 0.0)
    components = result.get("components", {})
    confidence = result.get("confidence", 0.0)

    aic_score = int(max(0, min(1000, 1000 * normalized)))
    rating = classify_aic(aic_score)

    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO scores (
            entity_name,
            aic_score,
            rating,
            semantic_intelligence,
            cultural_momentum,
            external_credibility,
            sentiment_stability,
            system_confidence,
            confidence,
            timestamp
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, datetime('now'))
        """,
        (
            entity_name,
            aic_score,
            rating,
            components.get("semantic_intelligence"),
            components.get("cultural_momentum"),
            components.get("external_credibility"),
            components.get("sentiment_stability"),
            components.get("system_confidence"),
            confidence,
        ),
    )
    conn.commit()

    return jsonify({
        "entity": entity_name,
        "aic_score": aic_score,
        "rating": rating,
        "components": components,
        "confidence": confidence
    })

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
