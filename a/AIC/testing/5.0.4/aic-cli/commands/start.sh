#!/bin/bash

# Define absolute paths (UPDATED for your actual structure)
PROJECT_ROOT="/home/userland/ABCd/a/AIC/testing/5.0.4"
PYTHON_DIR="$PROJECT_ROOT/engine-python"   # Changed from python-api to engine-python
NODE_DIR="$PROJECT_ROOT/backend-node"

echo "🚀 Starting AIC Backend..."

# --- 1. Stop any existing processes first ---
echo "   > Cleaning up previous instances..."
pm2 stop server 2>/dev/null
pm2 delete server 2>/dev/null

# Kill Python if running
if command -v pkill &> /dev/null; then
    pkill -f "python3 app.py" 2>/dev/null
fi

# --- 2. Start Python API ---
echo "   > Starting Python scoring engine..."

# Verify Python directory exists
if [ ! -d "$PYTHON_DIR" ]; then
    echo "❌ ERROR: Python directory not found at $PYTHON_DIR"
    echo "   Please update PROJECT_ROOT in start.sh"
    exit 1
fi

cd "$PYTHON_DIR"

# Start Python in background
python3 app.py &
PYTHON_PID=$!
echo "   > Python started (PID: $PYTHON_PID)"

# --- 3. Wait for Python to be ready ---
echo "   > Waiting for Python API to initialize..."
MAX_RETRIES=30
RETRY_COUNT=0

while [ $RETRY_COUNT -lt $MAX_RETRIES ]; do
    if curl -s -o /dev/null -w "%{http_code}" http://localhost:5000/ | grep -q "200\|404"; then
        echo "   > Python API is responsive!"
        break
    fi
    
    RETRY_COUNT=$((RETRY_COUNT + 1))
    sleep 1
done

if [ $RETRY_COUNT -eq $MAX_RETRIES ]; then
    echo "❌ ERROR: Python API failed to start after 30 seconds."
    kill $PYTHON_PID 2>/dev/null
    exit 1
fi

# --- 4. Start Node Backend ---
echo "   > Starting Node.js proxy..."

# Verify Node directory exists
if [ ! -d "$NODE_DIR" ]; then
    echo "❌ ERROR: Node directory not found at $NODE_DIR"
    exit 1
fi

cd "$NODE_DIR"

pm2 start server.js --name server
echo "   > Node.js proxy started."

# --- 5. Final Status ---
echo ""
echo "✅ AIC Backend is now running."
echo "   - Node API: http://localhost:3000"
echo "   - Python API: http://localhost:5000"
echo ""
pm2 list
