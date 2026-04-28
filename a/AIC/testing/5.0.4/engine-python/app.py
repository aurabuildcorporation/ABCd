from flask import Flask, request, jsonify
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from memory.rankings import leaderboard, compare, top_movers, percentile
from scorer import score_entity
from collector import collect_all_signals
from memory.store import init_db, save_score
from memory.trends import calculate_trend, get_entity_history

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

@app.route('/leaderboard')
def leaders():
    return jsonify(leaderboard())


@app.route('/compare/<a>/<b>')
def compare_entities(a, b):
    return jsonify(compare(a, b))


@app.route('/top-movers')
def movers():
    return jsonify(top_movers())


@app.route('/percentile/<entity>')
def entity_percentile(entity):
    return jsonify({
        "entity": entity,
        "percentile": percentile(entity)
    })

app.run(port=5000)
