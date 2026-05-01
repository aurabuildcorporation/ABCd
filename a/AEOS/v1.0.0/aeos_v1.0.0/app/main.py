from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from contextlib import asynccontextmanager
import os
import logging

from app.api.routes_admin import router as admin_router
from app.api import routes_ledger, routes_pi, routes_ae, routes_balance, routes_aic_events
from app.db.init_db import init_db
from app.db.event_store import init_event_store

logger = logging.getLogger("aeos")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("AEOS starting...")
    init_db()
    init_event_store()
    yield
    logger.info("AEOS shutting down...")

app = FastAPI(title="AEOS v2 Strict Mode", lifespan=lifespan)

app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/admin", response_class=HTMLResponse)
def admin_ui(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "mode": "admin"})

app.include_router(admin_router)
app.include_router(routes_aic_events.router)
app.include_router(routes_ledger.router)
app.include_router(routes_pi.router)
app.include_router(routes_ae.router)
app.include_router(routes_balance.router)
