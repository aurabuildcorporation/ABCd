# ============================================
# AIC Flask Dashboard V1
# Save as: app.py
# Run: python app.py
# ============================================

from flask import Flask, render_template_string, request, redirect
import requests
import sqlite3
from datetime import datetime

app = Flask(__name__)

DB = "aic_dashboard.db"
NODE_API = "http://localhost:3000/aic"

# ============================================
# DATABASE INIT
# ============================================
def init_db():
    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS queries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            query TEXT,
            score INTEGER,
            confidence REAL,
            created_at TEXT
        )
    """)

    conn.commit()
    conn.close()

init_db()

# ============================================
# HTML TEMPLATE
# ============================================
HTML = """
<!DOCTYPE html>
<html>
<head>
<title>AIC Dashboard</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<style>
body{
    background:#0b0f14;
    color:#e8f0ff;
    font-family:Arial;
    margin:40px;
}
h1{
    color:#67d7ff;
}
input{
    padding:10px;
    width:300px;
    background:#111827;
    color:white;
    border:1px solid #333;
}
button{
    padding:10px 16px;
    background:#1d4ed8;
    color:white;
    border:none;
    cursor:pointer;
}
.card{
    background:#111827;
    padding:20px;
    margin-top:20px;
    border-radius:8px;
}
table{
    width:100%;
    border-collapse:collapse;
    margin-top:20px;
}
td,th{
    padding:10px;
    border-bottom:1px solid #222;
}
th{
    color:#67d7ff;
}
canvas{
    background:#111827;
    margin-top:20px;
    padding:20px;
    border-radius:8px;
}
</style>
</head>
<body>

<h1>AIC Intelligence Dashboard</h1>

<form method="POST">
<input name="query" placeholder="Enter company / brand..." required>
<button type="submit">Get AIC</button>
</form>

{% if result %}
<div class="card">
<h2>{{result.query}}</h2>
<h3>AIC Score: {{result.score}}</h3>
<p>Confidence: {{result.confidence}}</p>
<p>{{result.time}}</p>
</div>
{% endif %}

<canvas id="chart" height="100"></canvas>

<div class="card">
<h2>Recent Queries</h2>
<table>
<tr>
<th>Query</th>
<th>Score</th>
<th>Confidence</th>
<th>Time</th>
</tr>

{% for row in rows %}
<tr>
<td>{{row[1]}}</td>
<td>{{row[2]}}</td>
<td>{{row[3]}}</td>
<td>{{row[4]}}</td>
</tr>
{% endfor %}
</table>
</div>

<script>
const labels = {{labels|safe}};
const values = {{values|safe}};

new Chart(document.getElementById('chart'), {
    type:'line',
    data:{
        labels:labels,
        datasets:[{
            label:'AIC Scores',
            data:values,
            tension:0.3
        }]
    },
    options:{
        plugins:{
            legend:{labels:{color:'white'}}
        },
        scales:{
            x:{ticks:{color:'white'}},
            y:{ticks:{color:'white'}}
        }
    }
});
</script>

</body>
</html>
"""

# ============================================
# ROUTE
# ============================================
@app.route("/", methods=["GET", "POST"])
def index():

    result = None

    if request.method == "POST":
        q = request.form["query"]

        try:
            r = requests.get(NODE_API, params={"query": q})
            data = r.json()

            score = data["aic_score"]
            confidence = data.get("confidence", 0.85)

            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            conn = sqlite3.connect(DB)
            cur = conn.cursor()

            cur.execute("""
                INSERT INTO queries
                (query, score, confidence, created_at)
                VALUES (?, ?, ?, ?)
            """, (q, score, confidence, now))

            conn.commit()
            conn.close()

            result = {
                "query": q,
                "score": score,
                "confidence": confidence,
                "time": now
            }

        except Exception as e:
            result = {
                "query": q,
                "score": "ERROR",
                "confidence": 0,
                "time": str(e)
            }

    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    cur.execute("""
        SELECT * FROM queries
        ORDER BY id DESC
        LIMIT 15
    """)

    rows = cur.fetchall()

    cur.execute("""
        SELECT query, score
        FROM queries
        ORDER BY id ASC
        LIMIT 25
    """)

    chart = cur.fetchall()

    conn.close()

    labels = [x[0] for x in chart]
    values = [x[1] for x in chart]

    return render_template_string(
        HTML,
        result=result,
        rows=rows,
        labels=labels,
        values=values
    )

# ============================================
# START
# ============================================
if __name__ == "__main__":
    app.run(debug=True, port=5000)
