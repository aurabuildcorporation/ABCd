from flask import Flask, request, jsonify, render_template
from db.database import init_db, save_score
import requests, os
app=Flask(__name__, template_folder="frontend/templates", static_folder="frontend/static")
ENGINE=os.getenv("NODEENGINEURL","http://localhost:4000")
init_db()
@app.route("/")
def index(): return render_template("index.html")
@app.route("/api/score", methods=["POST"])
def score():
    payload=request.get_json(force=True)
    r=requests.post(f"{ENGINE}/score", json=payload, timeout=20)
    data=r.json()
    save_score(data)
    return jsonify(data)
if __name__=="__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("FLASKPORT","5000")), debug=True)
