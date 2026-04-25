#!/bin/bash

echo "Checking AIC SCORE status..."

curl -s http://localhost:3000/score \
  -H "Content-Type: application/json" \
  -d '{"entity":"test"}' > /dev/null

if [ $? -eq 0 ]; then
  echo "Node API: OK"
else
  echo "Node API: DOWN"
fi

curl -s http://localhost:5000/score \
  -H "Content-Type: application/json" \
  -d '{"entity":"test"}' > /dev/null

if [ $? -eq 0 ]; then
  echo "Python Engine: OK"
else
  echo "Python Engine: DOWN"
fi
