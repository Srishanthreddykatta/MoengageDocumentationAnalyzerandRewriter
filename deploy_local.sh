#!/bin/bash

echo "========================================"
echo "Documentation Analyzer - Local Deploy"
echo "========================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    exit 1
fi

# Check if ngrok is installed
if ! command -v ngrok &> /dev/null; then
    echo ""
    echo "WARNING: ngrok is not installed!"
    echo ""
    echo "To install ngrok:"
    echo "  brew install ngrok  (Mac)"
    echo "  Or download from: https://ngrok.com/download"
    echo ""
    echo "Starting app without ngrok..."
    echo "You can access it at: http://localhost:5000"
    echo ""
    cd moengage_project/codebase
    python3 app.py
    exit 0
fi

# Navigate to codebase
cd moengage_project/codebase

# Check if dependencies are installed
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    playwright install chromium
else
    source venv/bin/activate
fi

echo ""
echo "Starting Flask application in background..."
python3 app.py &
FLASK_PID=$!

# Wait for Flask to start
sleep 5

echo ""
echo "Starting ngrok tunnel..."
ngrok http 5000 &
NGROK_PID=$!

echo ""
echo "========================================"
echo "Application is running!"
echo "========================================"
echo ""
echo "1. Flask app: http://localhost:5000"
echo "2. Check ngrok status at: http://localhost:4040"
echo "3. Your public URL will be shown in the ngrok dashboard"
echo ""
echo "Press Ctrl+C to stop both services..."
echo ""

# Wait for user interrupt
trap "kill $FLASK_PID $NGROK_PID 2>/dev/null; exit" INT TERM

# Keep script running
wait

