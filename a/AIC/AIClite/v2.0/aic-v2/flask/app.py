
from flask import Flask, request, render_template_string
import requests

app = Flask(__name__)

NODE = "http://localhost:3000/aic"

HTML = '''
<html>
<head>
<title>AIC Command Center</title>
<style>
body{background:#0b0f14;color:#0ff;font-family:monospace;}
.card{background:#111;padding:10px;margin:10px;}
</style>
<script>
async function refresh(){
  const rows = document.querySelectorAll(".row");
  rows.forEach(async r=>{
    let q = r.innerText;
    let res = await fetch("http://localhost:3000/aic?query="+q);
    let data = await res.json();
    r.innerHTML = q + " => " + data.aic_score + " " + data.trend;
  });
}
setInterval(refresh,5000);
</script>
</head>
<body>
<h1>AIC COMMAND CENTER</h1>

<form method="POST">
<input name="q"/>
<button>run</button>
</form>

{% if result %}
<div class="card">
{{result.query}} => {{result.aic_score}} {{result.trend}}
</div>
{% endif %}

<div class="card">
<h3>Watchlist</h3>
<div class="row">Nike</div>
<div class="row">Tesla</div>
<div class="row">OpenAI</div>
</div>

</body>
</html>
'''

@app.route("/",methods=["GET","POST"])
def home():
    result=None
    if request.method=="POST":
        q=request.form["q"]
        r=requests.get(NODE+"?query="+q).json()
        result=r
    return render_template_string(HTML,result=result)

app.run(port=5000,debug=True)
