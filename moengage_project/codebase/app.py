#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Flask web application for analyzing documentation from any website.
"""
import os
import logging
import json
from flask import Flask, render_template, request, jsonify
from urllib.parse import urlparse
from scraper import fetch_article_content
from readability import analyze_readability
from structure import analyze_structure
from completeness import analyze_completeness
from style import analyze_style
from reporter import generate_markdown_report, generate_json_report
from revision_agent import main_revision
import tempfile

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Get the directory where this script is located
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')

app = Flask(__name__, template_folder=TEMPLATE_DIR)
app.secret_key = os.urandom(24)  # For session management

# Define output directory for temporary files
TEMP_OUTPUT_DIR = os.path.join(tempfile.gettempdir(), "doc_analyzer_output")
os.makedirs(TEMP_OUTPUT_DIR, exist_ok=True)

@app.route('/')
def index():
    """Render the main page with the form."""
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    """Handle the analysis request."""
    try:
        data = request.get_json()
        if not data or 'url' not in data:
            return jsonify({'error': 'URL is required'}), 400
        
        article_url = data['url'].strip()
        
        # Validate URL
        parsed_url = urlparse(article_url)
        if not parsed_url.scheme in ["http", "https"]:
            return jsonify({'error': 'Invalid URL. Please provide a valid HTTP or HTTPS URL.'}), 400
        
        logging.info(f"Starting analysis for URL: {article_url}")
        
        # Step 1: Fetch Article Content
        logging.info(f"Fetching content for URL: {article_url}")
        article_content = fetch_article_content(article_url)
        
        if not article_content:
            return jsonify({'error': 'Failed to fetch article content. Please check the URL and try again.'}), 500
        
        logging.info("Article content fetched successfully.")
        
        # Step 2: Perform Analyses
        analysis_results = {}
        logging.info("Starting analysis...")
        
        try:
            analysis_results["Readability"] = analyze_readability(article_content)
            analysis_results["Structure"] = analyze_structure(article_content)
            analysis_results["Completeness"] = analyze_completeness(article_content)
            analysis_results["Style"] = analyze_style(article_content)
            logging.info("All analyses performed.")
        except Exception as e:
            logging.error(f"Error during analysis: {e}")
            return jsonify({'error': f'Analysis failed: {str(e)}'}), 500
        
        # Step 3: Generate Reports
        try:
            markdown_report = generate_markdown_report(article_url, analysis_results)
            json_report = generate_json_report(article_url, analysis_results)
            
            # Parse JSON report for easier frontend consumption
            json_data = json.loads(json_report) if json_report.strip().startswith("{") else None
            
            # Step 4: Generate Revised Article (optional, can be slow)
            revised_content = None
            if json_data:
                try:
                    # Create temporary file for JSON report
                    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False, dir=TEMP_OUTPUT_DIR) as tmp_file:
                        tmp_file.write(json_report)
                        tmp_json_path = tmp_file.name
                    
                    # Create temporary file for revised output
                    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False, dir=TEMP_OUTPUT_DIR) as tmp_revised:
                        tmp_revised_path = tmp_revised.name
                    
                    revised_content = main_revision(
                        original_article_url=article_url,
                        json_report_path=tmp_json_path,
                        output_revision_path=tmp_revised_path
                    )
                    
                    # Clean up temp files
                    try:
                        os.unlink(tmp_json_path)
                        if os.path.exists(tmp_revised_path):
                            os.unlink(tmp_revised_path)
                    except:
                        pass
                        
                except Exception as rev_e:
                    logging.warning(f"Revision generation failed: {rev_e}")
                    # Continue without revised content
            
            return jsonify({
                'success': True,
                'url': article_url,
                'markdown_report': markdown_report,
                'json_report': json_data,
                'revised_content': revised_content,
                'original_content_preview': article_content[:500] + "..." if len(article_content) > 500 else article_content
            })
            
        except Exception as e:
            logging.error(f"Error generating reports: {e}")
            return jsonify({'error': f'Report generation failed: {str(e)}'}), 500
            
    except Exception as e:
        logging.error(f"Unexpected error in analyze endpoint: {e}")
        return jsonify({'error': f'An unexpected error occurred: {str(e)}'}), 500

@app.route('/health')
def health():
    """Health check endpoint."""
    return jsonify({'status': 'healthy'}), 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)

