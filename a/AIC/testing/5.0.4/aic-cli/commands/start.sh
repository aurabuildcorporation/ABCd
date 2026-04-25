#!/bin/bash

echo "Starting AIC SCORE system..."

cd ../backend-node && node server.js &
cd ../engine-python && python3 app.py &

echo "Node + Python started"
echo "Angular: run manually with ng serve"
