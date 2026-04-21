#!/bin/bash
echo "[AIC-V3] Starting Flask server..."
export FLASK_APP=app.py
export FLASK_ENV=development
python3 app.py