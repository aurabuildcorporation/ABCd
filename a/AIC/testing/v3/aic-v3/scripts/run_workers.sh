#!/bin/bash
echo "[AIC-V3] Starting workers..."

python3 workers/run_interval.py &
PID1=$!

python3 workers/anomaly_detector.py &
PID2=$!

python3 workers/trend_tracker.py &
PID3=$!

python3 workers/forecast_worker.py &
PID4=$!

echo "Workers running (PIDs: $PID1, $PID2, $PID3, $PID4)"
wait