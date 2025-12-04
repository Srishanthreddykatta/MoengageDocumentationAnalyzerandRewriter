@echo off
echo ========================================
echo Documentation Analyzer - Local Deploy
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    pause
    exit /b 1
)

REM Check if ngrok is installed
where ngrok >nul 2>&1
if errorlevel 1 (
    echo.
    echo WARNING: ngrok is not installed!
    echo.
    echo To install ngrok:
    echo 1. Download from: https://ngrok.com/download
    echo 2. Or run: winget install ngrok
    echo.
    echo Starting app without ngrok...
    echo You can access it at: http://localhost:5000
    echo.
    goto :start_app
)

echo.
echo Starting Flask application...
echo.

cd moengage_project\codebase

REM Start Flask app in background
start "Flask App" cmd /k "python app.py"

REM Wait a bit for Flask to start
timeout /t 5 /nobreak >nul

echo.
echo Starting ngrok tunnel...
echo.

REM Start ngrok
start "ngrok" cmd /k "ngrok http 5000"

echo.
echo ========================================
echo Application is starting!
echo ========================================
echo.
echo 1. Flask app: http://localhost:5000
echo 2. Check the ngrok window for your public URL
echo 3. The ngrok URL will look like: https://xxxx.ngrok-free.app
echo.
echo Press any key to open ngrok dashboard...
pause >nul

REM Open ngrok dashboard
start http://localhost:4040

echo.
echo ========================================
echo To stop: Close the Flask and ngrok windows
echo ========================================
pause

