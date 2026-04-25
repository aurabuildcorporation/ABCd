#!/bin/bash

ENTITY=$1

if [ -z "$ENTITY" ]; then
  echo "Usage: aic score <entity>"
  exit 1
fi

echo "Scoring: $ENTITY"

curl -s -X POST http://localhost:3000/score \
  -H "Content-Type: application/json" \
  -d "{\"entity\":\"$ENTITY\"}" | jq
