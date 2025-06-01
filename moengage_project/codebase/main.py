#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import os
import logging
from urllib.parse import urlparse
from revision_agent import main_revision

# Import necessary functions from other modules
from scraper import fetch_article_content
from readability import analyze_readability
from structure import analyze_structure
from completeness import analyze_completeness
from style import analyze_style
# Import both report generation functions
from reporter import generate_markdown_report, generate_json_report 

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Define output directory relative to the script location
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
# Default output directory is one level up from script dir, in an 'output' folder
DEFAULT_OUTPUT_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, "..", "output")) 

def main():
    parser = argparse.ArgumentParser(description="Analyze MoEngage documentation articles.")
    parser.add_argument("url", help="The URL of the MoEngage documentation article to analyze.")
    parser.add_argument("-o", "--output", help=f"Directory to save the reports (default: adjacent 'output' folder)", default=DEFAULT_OUTPUT_DIR)
    # Add an option to control output format if desired (e.g., --format json/md/both)
    # parser.add_argument("--format", choices=["json", "md", "both"], default="both", help="Output format for the report")

    args = parser.parse_args()
    article_url = args.url
    output_dir = args.output
    # output_format = args.format # Uncomment if adding format argument

    # --- Validate URL (basic check) ---
    parsed_url_check = urlparse(article_url)
    if not parsed_url_check.scheme in ["http", "https"] or "help.moengage.com" not in parsed_url_check.netloc:
        logging.error(f"Invalid URL provided: {article_url}. Please provide a valid MoEngage help article URL.")
        return

    # --- Ensure output directory exists ---
    try:
        os.makedirs(output_dir, exist_ok=True)
        logging.info(f"Output directory set to: {output_dir}")
    except OSError as e:
        logging.error(f"Error creating output directory {output_dir}: {e}")
        return

    # --- Step 1: Fetch Article Content ---
    logging.info(f"Fetching content for URL: {article_url}")
    article_content = fetch_article_content(article_url)

    if not article_content:
        logging.error("Failed to fetch article content. Exiting.")
        return
    
    logging.info("Article content fetched successfully.")

    # --- Step 2: Perform Analyses ---
    analysis_results = {}
    logging.info("Starting analysis...")
    analysis_results["Readability"] = analyze_readability(article_content)
    analysis_results["Structure"] = analyze_structure(article_content)
    analysis_results["Completeness"] = analyze_completeness(article_content)
    analysis_results["Style"] = analyze_style(article_content)
    logging.info("All analyses performed.")

    # --- Step 3 & 4: Generate and Save Reports ---
    
    # Create a base filename from the URL path
    parsed_url = urlparse(article_url) 
    path_parts = [part for part in parsed_url.path.split("/") if part] 
    base_filename = path_parts[-1] if path_parts else "analysis_report"
    # Sanitize filename
    safe_filename = "".join(c if c.isalnum() or c in (".", "-", "_") else "_" for c in base_filename)

    # Generate and Save Markdown Report (Optional: control with --format arg)
    # if output_format in ["md", "both"]:
    logging.info(f"Generating Markdown report for {article_url}...")
    markdown_report = generate_markdown_report(article_url, analysis_results)
    if markdown_report:
        logging.info(f"Markdown report generated successfully for {article_url}.")
        report_filename_md = f"{safe_filename}_analysis.md"
        report_filepath_md = os.path.join(output_dir, report_filename_md)
        try:
            with open(report_filepath_md, "w", encoding="utf-8") as f:
                f.write(markdown_report)
            logging.info(f"Markdown analysis report saved successfully to: {report_filepath_md}")
        except IOError as e:
            logging.error(f"Error saving Markdown report file {report_filepath_md}: {e}")
    else:
        logging.error(f"Failed to generate Markdown report for {article_url}.")

    # Generate and Save JSON Report (Optional: control with --format arg)
    # if output_format in ["json", "both"]:
    logging.info(f"Generating JSON report for {article_url}...")
    json_report = generate_json_report(article_url, analysis_results)
    if json_report:
        # Check if the returned string is actually JSON or an error fallback
        # A simple check might be if it starts with '{'
        if json_report.strip().startswith("{"):
             logging.info(f"JSON report generated successfully for {article_url}.")
             report_filename_json = f"{safe_filename}_analysis.json"
             report_filepath_json = os.path.join(output_dir, report_filename_json)
             try:
                 with open(report_filepath_json, "w", encoding="utf-8") as f:
                     f.write(json_report)
                 logging.info(f"JSON analysis report saved successfully to: {report_filepath_json}")
             except IOError as e:
                 logging.error(f"Error saving JSON report file {report_filepath_json}: {e}")
             else:
                 # --- Step 5: Automatically Revise Article based on JSON Report ---
                 # This block executes only if the JSON was saved successfully
                 logging.info(f"Starting automatic revision for {article_url} based on {report_filepath_json}...")
                 revised_article_output_path_txt = os.path.join(output_dir, f"{safe_filename}_revised.txt") # Save as Text
                 revised_article_output_path_md = os.path.join(output_dir, f"{safe_filename}_revised.md") # Save as Markdown
                 try:
                     # Call the main revision function from revision_agent
                     revised_content = main_revision(original_article_url=article_url, json_report_path=report_filepath_json, output_revision_path=revised_article_output_path_txt) # Saves TXT
                     if revised_content:
                         # Save the same content as Markdown
                         try:
                             with open(revised_article_output_path_md, "w", encoding="utf-8") as md_f:
                                 md_f.write(revised_content)
                             logging.info(f"Also saved revised article as Markdown: {revised_article_output_path_md}")
                         except IOError as md_e:
                             logging.error(f"Error saving revised article as Markdown {revised_article_output_path_md}: {md_e}")
                     logging.info(f"Revision process completed for {article_url}.")
                 except Exception as rev_e:
                     logging.error(f"Error during automatic revision for {article_url}: {rev_e}")

        else:
            # Handle case where generate_json_report returned an error string instead of JSON
            logging.error(f"Failed to generate valid JSON report content for {article_url}. Content: {json_report[:100]}...") 
    else:
         logging.error(f"Failed to generate JSON report for {article_url} (function returned None).")

if __name__ == "__main__":
    # Check for API key before running main logic
    api_key_present = os.getenv("GOOGLE_API_KEY", "YOUR_API_KEY") != "YOUR_API_KEY"
    if not api_key_present:
        logging.warning("GOOGLE_API_KEY environment variable not set or using placeholder.")
    main() 

