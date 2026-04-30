
from fastapi import FastAPI
from app.api import routes_ledger, routes_pi, routes_ae

app = FastAPI(title="AEOS v2 Strict Mode")

app.include_router(routes_ledger.router)
app.include_router(routes_pi.router)
app.include_router(routes_ae.router)

@app.get("/")
def root():
    return {"status": "AEOS strict mode active"}
