#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import logging
import os
import re # Import re for link handling
from urllib.parse import urlparse

# Assuming llm_analyzer is in the same directory or accessible via PYTHONPATH
from llm_analyzer import analyze_text_with_llm, API_KEY, model as gemini_model
from scraper import fetch_article_content

# Corrected logging format string
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Updated prompt with explicit instruction to preserve links
REVISION_PROMPT_TEMPLATE = """
**Task:** Revise the following Original Article Content based *only* on the provided Suggestions for Improvement. Apply the suggestions thoughtfully to enhance the document's quality according to the criteria mentioned (readability for marketers, structure, completeness, style).

**IMPORTANT INSTRUCTION:** Preserve *all* original hyperlinks (e.g., `[link text](URL)` or HTML `<a>` tags) exactly as they appear in the original content. Do not modify, remove, or summarize links.

**Instructions:**
1.  Read the Original Article Content carefully.
2.  Review all the Suggestions for Improvement provided below, categorized by analysis type.
3.  Incorporate the *intent* of the suggestions into the original text. You may need to rephrase, add, remove, or restructure content.
4.  **Crucially, ensure all original hyperlinks are maintained in their original form and position relative to the surrounding text.**
5.  Do NOT introduce new information or topics not covered by the suggestions or original text.
6.  Aim for a natural, coherent, and improved version of the original article.
7.  Output *only* the complete revised article text. Do not include any introductory phrases, explanations, or markdown formatting around the revised text itself.

**Suggestions for Improvement:**

{suggestions_formatted}

**Original Article Content:**

```text
{original_article}
```

**Revised Article Content (Output only the revised text below, preserving all original hyperlinks):**
"""

def load_json_report(filepath: str) -> dict | None:
    """Loads the JSON analysis report (new format)."""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            report_data = json.load(f)
        # Validate basic structure
        if not all(k in report_data for k in ["url", "timestamp", "overall_score", "analysis"]):
            raise ValueError("JSON report missing top-level keys.")
        if not isinstance(report_data["analysis"], dict):
             raise ValueError("JSON report 'analysis' section is not a dictionary.")
        logging.info(f"Successfully loaded JSON report from: {filepath}")
        return report_data
    except FileNotFoundError:
        logging.error(f"JSON report file not found: {filepath}")
        return None
    except (json.JSONDecodeError, ValueError) as e:
        logging.error(f"Error decoding or validating JSON report {filepath}: {e}")
        return None
    except Exception as e:
        logging.error(f"Error loading JSON report {filepath}: {e}")
        return None

def format_suggestions_for_prompt(analysis_data: dict) -> str:
    """Formats the suggestions from the analysis dict into a string for the LLM prompt."""
    formatted = ""
    key_map = {
        "readability": "Readability",
        "structure": "Structure",
        "completeness": "Completeness",
        "style_guidelines": "Style Guidelines"
    }
    for key, display_name in key_map.items():
        if key in analysis_data and isinstance(analysis_data[key], dict):
            suggestions = analysis_data[key].get("suggestions", [])
            if suggestions and isinstance(suggestions, list):
                formatted += f"### {display_name} Suggestions:\n"
                for sugg in suggestions:
                    if isinstance(sugg, str):
                        formatted += f"- {sugg}\n"
                formatted += "\n"
    return formatted.strip() if formatted else "No specific suggestions provided."

def revise_entire_article(original_article: str, analysis_data: dict) -> str | None:
    """Uses the LLM to revise the entire article based on structured suggestions, instructing it to preserve links."""
    if not gemini_model:
        logging.error("Gemini model not initialized. Cannot revise text.")
        return None

    suggestions_formatted = format_suggestions_for_prompt(analysis_data)
    if not suggestions_formatted or suggestions_formatted == "No specific suggestions provided.":
        logging.warning("No actionable suggestions found in the report. Skipping revision.")
        # Return original article if no suggestions
        return original_article

    full_prompt = REVISION_PROMPT_TEMPLATE.format(
        suggestions_formatted=suggestions_formatted,
        original_article=original_article
    )

    logging.info("Sending request to LLM for full article revision (with link preservation instruction)...")
    # Use analyze_text_with_llm, passing the combined prompt. The 'text_content' arg is unused here.
    revised_text = analyze_text_with_llm(prompt=full_prompt, text_content="")

    if revised_text and not revised_text.startswith("Error:"):
        logging.info("LLM revision completed successfully.")
        # Basic cleanup - remove potential markdown code block fences if LLM added them
        cleaned_text = revised_text.strip()
        if cleaned_text.startswith("```text"):
             cleaned_text = cleaned_text[len("```text"):].strip()
        if cleaned_text.startswith("```"):
             cleaned_text = cleaned_text[3:].strip()
        if cleaned_text.endswith("```"):
             cleaned_text = cleaned_text[:-3].strip()
        
        # Note: Relying on LLM to preserve links. Further post-processing could be added
        # here to verify/restore links if needed, but it's complex.
        logging.info("Revision agent relies on LLM prompt instruction for link preservation.")
        
        return cleaned_text
    else:
        logging.error(f"LLM revision failed. Error: {revised_text}")
        return None

def main_revision(
    original_article_url: str, json_report_path: str, output_revision_path: str
):
    """Main function to drive the revision process using the new approach."""

    logging.info(f"Starting revision process for URL: {original_article_url}")
    logging.info(f"Using JSON report: {json_report_path}")

    # 1. Load Inputs
    report_data = load_json_report(json_report_path)
    if not report_data:
        logging.error("Failed to load or validate JSON report. Cannot proceed with revision.")
        return # Stop if report is invalid

    logging.info("Fetching original article content...")
    # Assuming fetch_article_content returns text with links preserved (e.g., markdown)
    original_article = fetch_article_content(original_article_url)
    if not original_article:
        logging.error("Failed to fetch original article content. Cannot proceed with revision.")
        return

    # 2. Perform Revision
    analysis_section = report_data.get("analysis")
    if not analysis_section or not isinstance(analysis_section, dict):
        logging.error("Invalid or missing 'analysis' section in JSON report. Cannot proceed.")
        return

    revised_article_content = revise_entire_article(original_article, analysis_section)

    # 3. Save Output
    if revised_article_content:
        try:
            # Ensure output directory exists
            os.makedirs(os.path.dirname(output_revision_path), exist_ok=True)
            with open(output_revision_path, "w", encoding="utf-8") as f:
                f.write(revised_article_content)
            logging.info(f"Revised article saved successfully to: {output_revision_path}")
            return revised_article_content # Return content after successful save
        except IOError as e:
            logging.error(f"Error saving revised article file {output_revision_path}: {e}")
            return None # Return None on save error
    else:
        logging.warning(f"Revision process did not produce output. No file saved to {output_revision_path}")
        return None # Return None if revision failed


if __name__ == "__main__":
    # Example usage - requires a pre-existing JSON report from Task 1
    # Ensure GOOGLE_API_KEY is set in the environment

    # Determine paths relative to the script location
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # Assume output dir is one level up from where the script is (e.g., project root/output)
    output_dir = os.path.abspath(os.path.join(script_dir, "..", "output"))
    # If scripts are in root, output dir is ./output
    if not os.path.exists(output_dir):
         output_dir = os.path.join(script_dir, "output") # Fallback to output dir in script dir

    # --- Configuration for Testing --- 
    # Use a URL for which a report is expected to exist
    test_url = "https://help.moengage.com/hc/en-us/articles/33436161901332-Sign-Up-with-MoEngage-or-Create-a-New-Account-in-MoEngage"

    # Construct the expected JSON report filename based on the URL
    parsed_url = urlparse(test_url)
    path_parts = [part for part in parsed_url.path.split("/") if part and part != 'articles']
    base_filename = path_parts[-1] if path_parts else "default_report"
    safe_filename = "".join(c if c.isalnum() or c in (".", "-", "_") else "_" for c in base_filename)
    # Match the filename generated by main.py
    json_filename = f"{safe_filename}_analysis.json"
    json_report_input_path = os.path.join(output_dir, json_filename)

    # Define the output path for the revised text
    revised_article_output_path = os.path.join(output_dir, f"{safe_filename}_revised.txt")
    # --- End Configuration --- 

    print(f"Attempting to revise based on report: {json_report_input_path}")
    print(f"Revised article will be saved to: {revised_article_output_path}")

    if not os.path.exists(json_report_input_path):
        print(f"\nERROR: JSON report not found at expected location: {json_report_input_path}")
        print("Please run the main analysis agent (main.py) first to generate the report.")
    elif API_KEY == "YOUR_API_KEY" or not gemini_model:
        print("\nERROR: GOOGLE_API_KEY not configured or Gemini model not initialized.")
        print("Please set the environment variable and ensure llm_analyzer is configured.")
    else:
        print("\nStarting revision agent...")
        os.makedirs(output_dir, exist_ok=True) # Ensure output dir exists
        main_revision(test_url, json_report_input_path, revised_article_output_path)
        print("\nRevision agent finished.")

