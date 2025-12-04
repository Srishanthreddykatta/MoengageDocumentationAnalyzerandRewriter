#!/bin/bash

echo "========================================"
echo "GitHub Setup Helper"
echo "========================================"
echo ""

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo "ERROR: Git is not installed!"
    echo "Please install Git from: https://git-scm.com/downloads"
    exit 1
fi

echo "Step 1: Initialize Git repository..."
if [ -d .git ]; then
    echo "Git repository already exists."
else
    git init
    echo "Git repository initialized."
fi

echo ""
echo "Step 2: Adding all files..."
git add .

echo ""
echo "Step 3: Creating initial commit..."
git commit -m "Initial commit - Documentation Analyzer with web interface"

echo ""
echo "========================================"
echo "Next Steps:"
echo "========================================"
echo ""
echo "1. Create a new repository on GitHub:"
echo "   https://github.com/new"
echo ""
echo "2. Name it: documentation-analyzer"
echo "   Make it PUBLIC so your friend can access"
echo ""
echo "3. Run these commands (replace YOUR_USERNAME):"
echo ""
echo "   git remote add origin https://github.com/YOUR_USERNAME/documentation-analyzer.git"
echo "   git branch -M main"
echo "   git push -u origin main"
echo ""
echo "4. Then follow GITHUB_DEPLOYMENT.md to deploy!"
echo ""
echo "========================================"

