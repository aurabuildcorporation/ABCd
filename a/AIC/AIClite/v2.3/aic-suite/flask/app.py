
from flask import Flask, render_template, request, Response
from flask_socketio import SocketIO
import requests
import json
import csv
import io
import threading
import time

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

NODE = "http://localhost:3000/aic"

watchlist = ["Nike", "Tesla", "OpenAI"]

def fetch(q):
    try:
        return requests.get(NODE, params={"query": q}).json()
    except:
        return {"aic_score":0,"trend":"?"}

def loop():
    while True:
        data=[]
        for e in watchlist:
            r=fetch(e)
            data.append({
                "entity":e,
                "score":r.get("aic_score",0),
                "trend":r.get("trend","?")
            })
        socketio.emit("watchlist_update",data)
        time.sleep(5)

@app.route("/")
def home():
    return render_template("dashboard.html")

@app.route("/export/csv")
def export_csv():
    out=io.StringIO()
    w=csv.writer(out)
    w.writerow(["entity","score","trend"])
    for e in watchlist:
        r=fetch(e)
        w.writerow([e,r.get("aic_score"),r.get("trend")])
    return Response(out.getvalue(),mimetype="text/csv",
        headers={"Content-Disposition":"attachment;filename=aic.csv"})

@app.route("/export/json")
def export_json():
    data=[]
    for e in watchlist:
        r=fetch(e)
        data.append({"entity":e,"score":r.get("aic_score"),"trend":r.get("trend")})
    return Response(json.dumps(data,indent=2),
        mimetype="application/json",
        headers={"Content-Disposition":"attachment;filename=aic.json"})

@app.route("/export/txt")
def export_txt():
    lines=["AIC REPORT"]
    for e in watchlist:
        r=fetch(e)
        lines.append(f"{e}: {r.get('aic_score')} {r.get('trend')}")
    return Response("\n".join(lines),
        mimetype="text/plain",
        headers={"Content-Disposition":"attachment;filename=aic.txt"})

@socketio.on("query")
def handle(data):
    q=data.get("q","")
    socketio.emit("result",fetch(q))

if __name__=="__main__":
    t=threading.Thread(target=loop)
    t.daemon=True
    t.start()
    socketio.run(app,port=5000,debug=True)
