#!/bin/bash

echo "Stopping AIC SCORE..."

fuser -k 3000/tcp
fuser -k 5000/tcp
fuser -k 4200/tcp

echo "All services stopped."
