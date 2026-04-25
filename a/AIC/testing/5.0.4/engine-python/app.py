from flask import Flask, request, jsonify

from scorer import score_entity
from collector import collect_all_signals
from memory.store import init_db, save_score
from memory.trends import calculate_trend
from memory.trends import get_entity_history, calculate_trend

app = Flask(__name__)

init_db()  # initialize SQLite on startup


@app.route('/score', methods=['POST'])
def score():

    entity = request.json["entity"]

    # 1. collect signals
    signals = collect_all_signals(entity)

    # 2. compute score
    result = score_entity(entity, signals)

    # 3. save to memory
    save_score(entity, result)

    # 4. compute trend
    trend = calculate_trend(entity)

    # 5. attach memory output
    result["trend"] = trend

    return jsonify(result)

@app.route('/history/<entity>', methods=['GET'])
def history(entity):

    data = get_entity_history(entity, 10)
    trend = calculate_trend(entity)

    return jsonify({
        "entity": entity,
        "history": data,
        "trend": trend
    })

app.run(port=5000)
