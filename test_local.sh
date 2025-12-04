#!/bin/bash

echo "Testing Documentation Analyzer locally..."
echo ""

cd moengage_project/codebase

echo "Checking Python..."
python3 --version || { echo "ERROR: Python 3 not found!"; exit 1; }

echo ""
echo "Installing/updating dependencies..."
pip3 install -r requirements.txt

echo ""
echo "Installing Playwright browsers..."
playwright install chromium

echo ""
echo "Starting Flask application..."
echo "Open http://localhost:5000 in your browser"
echo "Press Ctrl+C to stop"
echo ""

python3 app.py

