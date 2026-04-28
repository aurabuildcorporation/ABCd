#!/bin/bash
echo "Checking AIC SCORE status..."

# Check Node API Health (Check for 200 or 503, not just connection)
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:3000/history/test)

if [ "$HTTP_CODE" = "200" ]; then
  echo "Node API: ONLINE (Healthy)"
elif [ "$HTTP_CODE" = "503" ]; then
  echo "Node API: ONLINE (Degraded - Python Offline)"
else
  echo "Node API: DOWN (Code: $HTTP_CODE)"
fi

# Check Python Engine
HTTP_PYTHON=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:5000/)

if [ "$HTTP_PYTHON" = "200" ] || [ "$HTTP_PYTHON" = "404" ]; then
  echo "Python Engine: ONLINE"
else
  echo "Python Engine: DOWN (Code: $HTTP_PYTHON)"
fi

# Show PM2 status if available
if command -v pm2 &> /dev/null; then
    echo "--- PM2 Status ---"
    pm2 list 2>/dev/null || echo "PM2 not running or empty"
fi
