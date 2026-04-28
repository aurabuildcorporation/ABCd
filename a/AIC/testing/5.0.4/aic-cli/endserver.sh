# 1. Kill all Node processes (Force kill PM2)
pm2 kill

# 2. Kill any remaining Node processes on port 3000
# (Using lsof since fuser is missing)
if command -v lsof &> /dev/null; then
    PID=$(lsof -t -i:3000)
    if [ ! -z "$PID" ]; then
        kill -9 $PID
        echo "Killed Node on port 3000 (PID: $PID)"
    fi
fi

# 3. Kill any remaining Python processes
pkill -9 -f "python3 app.py"

# 4. Verify nothing is running
pm2 list
lsof -i :3000
lsof -i :5000
