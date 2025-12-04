@echo off
REM Startup script for Windows

echo Starting Documentation Analyzer...

cd moengage_project\codebase

REM Check if virtual environment exists
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt

REM Install Playwright browsers
echo Installing Playwright browsers...
playwright install chromium

REM Run the application
echo Starting Flask application...
python app.py

pause

