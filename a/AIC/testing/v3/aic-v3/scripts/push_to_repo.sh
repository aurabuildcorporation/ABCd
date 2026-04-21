#!/bin/bash

echo "[AIC-V3] Committing and pushing to GitHub..."

git add .
git commit -m "AIC-V3 update"
git push origin main

echo "[AIC-V3] Push complete."