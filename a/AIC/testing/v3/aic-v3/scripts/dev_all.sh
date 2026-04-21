#!/bin/bash
echo "[AIC-V3] Starting full development stack..."

# Start Node engine
(cd engine && npm install --silent && node server.js) &
NODE_PID=$!

# Start Flask
(python3 app.py) &
FLASK_PID=$!

# Start workers
(bash scripts/run_workers.sh) &
WORKERS_PID=$!

echo "Dev stack running:"
echo "  Node:   $NODE_PID"
echo "  Flask:  $FLASK_PID"
echo "  Workers: $WORKERS_PID"

wait