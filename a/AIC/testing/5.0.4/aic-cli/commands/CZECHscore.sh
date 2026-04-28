#!/bin/bash

# =====================================================
# AIC CLI - score.sh v5.0.4
# Direct scoring request to Node backend
# Mirrors working curl test exactly
# =====================================================

ENTITY="$*"
API_URL="http://localhost:3000/score"

GREEN="\e[32m"
RED="\e[31m"
CYAN="\e[36m"
NC="\e[0m"

line() {
    echo "====================================================="
}

# -----------------------------------------------------
# VALIDATE INPUT
# -----------------------------------------------------

if [ -z "$ENTITY" ]; then
    echo -e "${RED}❌ Missing entity${NC}"
    echo "Usage:"
    echo "  aic score Apple"
    echo "  aic score Tesla"
    echo "  aic score \"Microsoft Corp\""
    exit 1
fi

# -----------------------------------------------------
# HEADER
# -----------------------------------------------------

line
echo -e "${CYAN}AIC SCORE REQUEST${NC}"
line
echo "Entity: $ENTITY"
echo ""

# -----------------------------------------------------
# SEND REQUEST
# -----------------------------------------------------

RESPONSE=$(curl -s -X POST "$API_URL" \
-H "Content-Type: application/json" \
-d "{\"entity\":\"$ENTITY\"}")

# -----------------------------------------------------
# HANDLE FAILURE
# -----------------------------------------------------

if [ -z "$RESPONSE" ]; then
    echo -e "${RED}❌ No response from backend${NC}"
    echo "Run: aic start"
    exit 1
fi

# -----------------------------------------------------
# DISPLAY RESULT
# -----------------------------------------------------

echo -e "${GREEN}✅ Response:${NC}"
echo ""

echo "$RESPONSE" | python3 -m json.tool 2>/dev/null || echo "$RESPONSE"

echo ""
line
