@echo off
echo Testing Documentation Analyzer locally...
echo.

cd moengage_project\codebase

echo Checking Python...
python --version
if errorlevel 1 (
    echo ERROR: Python not found!
    pause
    exit /b 1
)

echo.
echo Installing/updating dependencies...
pip install -r requirements.txt

echo.
echo Installing Playwright browsers...
playwright install chromium

echo.
echo Starting Flask application...
echo Open http://localhost:5000 in your browser
echo Press Ctrl+C to stop
echo.

python app.py

pause

