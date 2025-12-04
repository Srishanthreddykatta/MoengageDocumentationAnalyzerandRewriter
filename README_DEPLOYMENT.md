# Documentation Analyzer - Deployment Guide

This application analyzes documentation from any website for readability, structure, completeness, and style using Google's Gemini Flash 2.0 API.

## Features

- ✅ Accepts any website URL (not just MoEngage)
- ✅ Web-based interface for easy use
- ✅ Real-time analysis with progress indicators
- ✅ Multiple output formats (Markdown, JSON, Revised Content)
- ✅ Docker support for easy deployment

## Quick Start with Docker

### Prerequisites
- Docker and Docker Compose installed

### Steps

1. **Clone/Navigate to the project directory**

2. **Build and run with Docker Compose:**
   ```bash
   docker-compose up --build
   ```

3. **Access the application:**
   Open your browser and navigate to: `http://localhost:5000`

## Manual Deployment

### Prerequisites
- Python 3.11 or later
- pip

### Steps

1. **Install dependencies:**
   ```bash
   cd moengage_project/codebase
   pip install -r requirements.txt
   playwright install chromium
   ```

2. **Run the application:**
   ```bash
   python app.py
   ```

3. **Access the application:**
   Open your browser and navigate to: `http://localhost:5000`

## Production Deployment

### Using Gunicorn (Recommended)

```bash
gunicorn --bind 0.0.0.0:5000 --workers 4 --timeout 300 app:app
```

### Environment Variables

- `PORT`: Port to run the application on (default: 5000)
- `GOOGLE_API_KEY`: Google API key (optional, default key is already configured)

## API Endpoints

### POST /analyze
Analyzes a website URL and returns analysis results.

**Request:**
```json
{
  "url": "https://example.com/docs/article"
}
```

**Response:**
```json
{
  "success": true,
  "url": "https://example.com/docs/article",
  "markdown_report": "...",
  "json_report": {...},
  "revised_content": "...",
  "original_content_preview": "..."
}
```

### GET /health
Health check endpoint.

## Configuration

The Google Gemini Flash 2.0 API key is pre-configured. To use a different key, set the `GOOGLE_API_KEY` environment variable.

## Troubleshooting

1. **Playwright browser issues:**
   - Make sure Playwright browsers are installed: `playwright install chromium`

2. **Port already in use:**
   - Change the port in `app.py` or set the `PORT` environment variable

3. **Analysis timeout:**
   - Increase the timeout in gunicorn command: `--timeout 600`

## License

This project is provided as-is for documentation analysis purposes.

