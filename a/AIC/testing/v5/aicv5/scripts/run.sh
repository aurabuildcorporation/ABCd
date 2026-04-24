#!/bin/bash
(cd engine && npm install && node server.js &) 
python app.py
