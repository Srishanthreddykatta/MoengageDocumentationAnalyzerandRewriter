# Quick Start Guide

## 🚀 Fastest Way to Run (Docker)

```bash
docker-compose up --build
```

Then open: http://localhost:5000

## 📝 Manual Setup

### Windows:
```bash
start.bat
```

### Linux/Mac:
```bash
chmod +x start.sh
./start.sh
```

### Or manually:
```bash
cd moengage_project/codebase
pip install -r requirements.txt
playwright install chromium
python app.py
```

## 🌐 Usage

1. Open http://localhost:5000 in your browser
2. Enter any website URL (e.g., https://example.com/docs)
3. Click "Analyze"
4. View results in the tabs:
   - **Analysis Report**: Human-readable markdown report
   - **JSON Data**: Structured JSON data
   - **Revised Content**: Improved version of the content

## 🔑 API Key

The Google Gemini Flash 2.0 API key is pre-configured. To use your own:
- Set environment variable: `GOOGLE_API_KEY=your_key_here`

## 🐳 Docker Deployment

```bash
# Build
docker build -t doc-analyzer .

# Run
docker run -p 5000:5000 doc-analyzer
```

## 📦 Production Deployment

For production, use Gunicorn:
```bash
gunicorn --bind 0.0.0.0:5000 --workers 4 --timeout 300 app:app
```

