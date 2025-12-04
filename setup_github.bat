@echo off
echo ========================================
echo GitHub Setup Helper
echo ========================================
echo.

REM Check if git is installed
git --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Git is not installed!
    echo Please install Git from: https://git-scm.com/download/win
    pause
    exit /b 1
)

echo Step 1: Initialize Git repository...
if exist .git (
    echo Git repository already exists.
) else (
    git init
    echo Git repository initialized.
)

echo.
echo Step 2: Creating .gitignore...
if exist .gitignore (
    echo .gitignore already exists.
) else (
    echo .gitignore will be created automatically.
)

echo.
echo Step 3: Adding all files...
git add .

echo.
echo Step 4: Creating initial commit...
git commit -m "Initial commit - Documentation Analyzer with web interface"

echo.
echo ========================================
echo Next Steps:
echo ========================================
echo.
echo 1. Create a new repository on GitHub:
echo    https://github.com/new
echo.
echo 2. Name it: documentation-analyzer
echo    Make it PUBLIC so your friend can access
echo.
echo 3. Run these commands (replace YOUR_USERNAME):
echo.
echo    git remote add origin https://github.com/YOUR_USERNAME/documentation-analyzer.git
echo    git branch -M main
echo    git push -u origin main
echo.
echo 4. Then follow GITHUB_DEPLOYMENT.md to deploy!
echo.
echo ========================================
pause

