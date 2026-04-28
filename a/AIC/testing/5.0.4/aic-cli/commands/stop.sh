#!/bin/bash

echo "Stopping AIC SCORE..."

# 1. Stop Node via PM2
pm2 stop server 2>/dev/null
pm2 delete server 2>/dev/null
echo "   > Node.js stopped."

# 2. Stop Python (Find PID by port 5000 and kill)
# Try lsof first, if not found, try pkill
if command -v lsof &> /dev/null; then
    PID=$(lsof -t -i:5000)
    if [ ! -z "$PID" ]; then
        kill -9 $PID
        echo "   > Python API stopped (Port 5000)."
    else
        echo "   > No Python process found on port 5000."
    fi
elif command -v pkill &> /dev/null; then
    pkill -f "python3 app.py"
    echo "   > Python API stopped (via pkill)."
else
    # Fallback: Just warn the user
    echo "   > Warning: Could not auto-stop Python (missing lsof/pkill). Please kill manually."
fi

echo "✅ All services stopped."
