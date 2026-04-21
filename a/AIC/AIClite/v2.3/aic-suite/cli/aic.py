
import sys, requests

cmd = sys.argv[1] if len(sys.argv)>1 else ""

if cmd == "rank":
    items = sys.argv[2:]
    r = requests.get("http://localhost:3000/rank", params={"list":",".join(items)}).json()
    print(r)

elif cmd == "watch":
    q = sys.argv[2]
    r = requests.get("http://localhost:3000/aic", params={"query":q}).json()
    print(q, r["aic_score"], r["trend"])

else:
    r = requests.get("http://localhost:3000/aic", params={"query":cmd}).json()
    print(r)
