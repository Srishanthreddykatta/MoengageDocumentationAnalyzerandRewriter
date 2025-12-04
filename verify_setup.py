#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Quick verification script to check if everything is set up correctly.
"""
import os
import sys

def check_file_exists(filepath, description):
    """Check if a file exists."""
    if os.path.exists(filepath):
        print(f"✅ {description}: Found")
        return True
    else:
        print(f"❌ {description}: NOT FOUND at {filepath}")
        return False

def check_import(module_name, description):
    """Check if a module can be imported."""
    try:
        __import__(module_name)
        print(f"✅ {description}: OK")
        return True
    except ImportError as e:
        print(f"❌ {description}: FAILED - {e}")
        return False

def main():
    print("=" * 50)
    print("Documentation Analyzer - Setup Verification")
    print("=" * 50)
    print()
    
    # Change to codebase directory
    codebase_dir = os.path.join(os.path.dirname(__file__), 'moengage_project', 'codebase')
    if not os.path.exists(codebase_dir):
        print(f"❌ Codebase directory not found: {codebase_dir}")
        return False
    
    os.chdir(codebase_dir)
    print(f"📁 Working directory: {codebase_dir}")
    print()
    
    # Check required files
    print("Checking required files...")
    files_ok = True
    files_ok &= check_file_exists('app.py', 'Flask application')
    files_ok &= check_file_exists('templates/index.html', 'HTML template')
    files_ok &= check_file_exists('requirements.txt', 'Requirements file')
    files_ok &= check_file_exists('scraper.py', 'Scraper module')
    files_ok &= check_file_exists('llm_analyzer.py', 'LLM analyzer')
    print()
    
    # Check Python version
    print("Checking Python version...")
    version = sys.version_info
    if version.major == 3 and version.minor >= 8:
        print(f"✅ Python version: {version.major}.{version.minor}.{version.micro}")
    else:
        print(f"⚠️  Python version: {version.major}.{version.minor}.{version.micro} (Recommended: 3.11+)")
    print()
    
    # Check imports
    print("Checking Python packages...")
    imports_ok = True
    imports_ok &= check_import('flask', 'Flask')
    imports_ok &= check_import('playwright', 'Playwright')
    imports_ok &= check_import('google.generativeai', 'Google Generative AI')
    print()
    
    # Check API key
    print("Checking API key configuration...")
    try:
        from llm_analyzer import API_KEY
        if API_KEY and API_KEY != "YOUR_API_KEY":
            print(f"✅ API Key: Configured (ends with ...{API_KEY[-4:]})")
        else:
            print("⚠️  API Key: Using default (should work)")
    except Exception as e:
        print(f"⚠️  API Key: Could not verify - {e}")
    print()
    
    # Summary
    print("=" * 50)
    if files_ok and imports_ok:
        print("✅ Setup looks good! You can run the app.")
        print()
        print("Next steps:")
        print("1. Run: python app.py")
        print("2. Or use: test_local.bat (Windows) / test_local.sh (Linux/Mac)")
        return True
    else:
        print("⚠️  Some issues found. Please install missing dependencies:")
        print("   pip install -r requirements.txt")
        print("   playwright install chromium")
        return False

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)

