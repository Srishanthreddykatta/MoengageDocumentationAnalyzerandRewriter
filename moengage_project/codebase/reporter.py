#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
import logging
import json
from collections import Counter

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Define score mapping for overall calculation
SCORE_MAP = {"Poor": 1, "Fair": 2, "Good": 3, "Error": 0} # Assign numerical values
INV_SCORE_MAP = {v: k for k, v in SCORE_MAP.items() if k != "Error"} # Map back, excluding Error

# Define default structures for error handling, matching the new formats
DEFAULT_ERROR_READABILITY = {
    "score": "Error", "assessment": "Readability analysis failed.", "issues": [], "suggestions": []
}
DEFAULT_ERROR_STRUCTURE = {
    "score": "Error", "assessment": "Structure analysis failed.",
    "counts": {"h1": 0, "h2": 0, "h3": 0, "paragraphs": 0, "lists": 0},
    "analysis": {"headings": "N/A", "paragraphs_lists": "N/A"},
    "flow_navigation": {"assessment": "N/A"},
    "issues": [], "suggestions": []
}
DEFAULT_ERROR_COMPLETENESS = {
    "score": "Error", "assessment": "Completeness analysis failed.", "issues": [], "suggestions": []
}
DEFAULT_ERROR_STYLE = {
    "score": "Error", "assessment": "Style analysis failed.",
    "analysis": {"voice_tone": "N/A", "clarity_conciseness": "N/A", "action_oriented_language": "N/A"},
    "issues": [], "suggestions": []
}

DEFAULT_ERROR_MAP = {
    "readability": DEFAULT_ERROR_READABILITY,
    "structure": DEFAULT_ERROR_STRUCTURE,
    "completeness": DEFAULT_ERROR_COMPLETENESS,
    "style_guidelines": DEFAULT_ERROR_STYLE
}

def calculate_overall_score(analysis_results: dict) -> str:
    """Calculates an overall score based on individual analysis scores."""
    scores = []
    has_error = False
    expected_keys = ["readability", "structure", "completeness", "style_guidelines"]
    for key in expected_keys:
        section_result = analysis_results.get(key)
        # Check if it's a dict and has a score
        if isinstance(section_result, dict) and "score" in section_result:
            score = section_result["score"]
            if score == "Error":
                has_error = True
                scores.append(SCORE_MAP["Fair"]) # Treat errors as Fair for averaging
            elif score in SCORE_MAP:
                scores.append(SCORE_MAP[score])
            else:
                 scores.append(SCORE_MAP["Fair"]) # Handle unexpected score values
        else:
            # Handle cases where a section result isn't a dict or lacks a score
            has_error = True # Treat missing/malformed data as an issue
            scores.append(SCORE_MAP["Fair"])

    if not scores: # No valid scores found
        return "N/A"
        
    average_score = round(sum(scores) / len(scores))
    overall_score_str = INV_SCORE_MAP.get(average_score, "Fair")

    if has_error and overall_score_str == "Good":
        return "Fair"
        
    # If all inputs resulted in errors or were missing
    if all(s == SCORE_MAP["Fair"] for s in scores) and has_error and len(scores) == len(expected_keys):
         return "Error"
         
    return overall_score_str

def generate_report(url: str, analyses: dict, output_format: str = "json") -> str:
    """Generates a report in the specified format (json or markdown)."""
    if output_format.lower() == "json":
        return generate_json_report(url, analyses)
    elif output_format.lower() == "markdown":
        return generate_markdown_report(url, analyses)
    else:
        logging.warning(f"Unsupported report format: {output_format}. Defaulting to JSON.")
        return generate_json_report(url, analyses)

def generate_json_report(url: str, analyses: dict) -> str:
    """Formats the analysis results into the specified JSON structure (using new detailed format)."""
    logging.info(f"Generating JSON report for {url} (using new detailed format)...")

    analysis_data = {}
    key_map = {
        "Readability": "readability",
        "Structure": "structure",
        "Completeness": "completeness",
        "Style": "style_guidelines"
    }

    # Validate and structure the analysis data according to the new format
    for input_key, output_key in key_map.items():
        if input_key in analyses and isinstance(analyses[input_key], dict):
            # Use the structure from the analysis module if valid, otherwise use default error
            # Basic validation happens within the analysis modules now
            analysis_data[output_key] = analyses[input_key]
        else:
            logging.warning(f"Analysis result for {input_key} not found or not a dict. Using error default.")
            # Use the specific default error structure for this section
            analysis_data[output_key] = DEFAULT_ERROR_MAP[output_key].copy()
            analysis_data[output_key]["issues"] = [f"Analysis data for {input_key} missing or not a dictionary."]

    overall_score = calculate_overall_score(analysis_data)

    report_data = {
        "url": url,
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "overall_score": overall_score,
        "analysis": analysis_data
    }

    try:
        json_output = json.dumps(report_data, indent=2)
        logging.info(f"JSON report generated successfully for {url}.")
        return json_output
    except TypeError as e:
        logging.error(f"Error serializing report data to JSON for {url}: {e}")
        # Fallback: return a JSON object with an error message and default structures
        error_data = {
            "url": url,
            "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "overall_score": "Error",
            "analysis": {key: DEFAULT_ERROR_MAP[key].copy() for key in key_map.values()},
            "error_details": f"Failed to generate JSON report: {str(e)}"
        }
        return json.dumps(error_data, indent=2)

def generate_markdown_report(url: str, analyses: dict) -> str:
    """Formats the analysis results into a Markdown report (using new detailed structured input)."""
    logging.info(f"Generating Markdown report for {url} (using new detailed format)...")

    report_content = f"# Documentation Analysis Report\n\n"
    report_content += f"**Analyzed URL:** {url}\n"
    report_content += f"**Analysis Timestamp:** {datetime.datetime.now(datetime.timezone.utc).isoformat()}\n\n"

    # Calculate overall score for the report
    temp_analysis_data_for_score = {}
    key_map = {
        "Readability": "readability",
        "Structure": "structure",
        "Completeness": "completeness",
        "Style": "style_guidelines"
    }
    output_key_map = {v: k for k, v in key_map.items()} # Map output key back to input key for lookup

    for input_key, output_key in key_map.items():
         # Use the actual analysis data passed in
         if input_key in analyses and isinstance(analyses[input_key], dict):
              temp_analysis_data_for_score[output_key] = analyses[input_key]
         else:
              # Add a placeholder if missing for score calculation consistency
              temp_analysis_data_for_score[output_key] = DEFAULT_ERROR_MAP[output_key].copy()

    overall_score = calculate_overall_score(temp_analysis_data_for_score)
    report_content += f"**Overall Score:** {overall_score}\n\n"
    report_content += "---\n\n"

    analysis_order = ["Readability", "Structure", "Completeness", "Style"]

    for key in analysis_order:
        report_content += f"## {key} Analysis\n\n"
        output_key = key_map.get(key)
        section_data = analyses.get(key)

        # Check if data exists and is a dictionary
        if isinstance(section_data, dict):
            # *** FIX: Use single quotes inside f-string ***
            report_content += f"**Score:** {section_data.get('score', 'N/A')}\n"
            report_content += f"**Assessment:** {section_data.get('assessment', 'N/A')}\n\n"

            # Handle Structure specific fields
            if key == "Structure":
                counts = section_data.get("counts", {})
                if isinstance(counts, dict):
                    report_content += f"**Counts:**\n"
                    report_content += f"  - H1: {counts.get('h1', 'N/A')}\n"
                    report_content += f"  - H2: {counts.get('h2', 'N/A')}\n"
                    report_content += f"  - H3: {counts.get('h3', 'N/A')}\n"
                    report_content += f"  - Paragraphs: {counts.get('paragraphs', 'N/A')}\n"
                    report_content += f"  - Lists: {counts.get('lists', 'N/A')}\n\n"
                analysis = section_data.get("analysis", {})
                if isinstance(analysis, dict):
                    report_content += f"**Sub-Analysis:**\n"
                    report_content += f"  - Headings: {analysis.get('headings', 'N/A')}\n"
                    report_content += f"  - Paragraphs/Lists: {analysis.get('paragraphs_lists', 'N/A')}\n\n"
                flow_nav = section_data.get("flow_navigation", {})
                if isinstance(flow_nav, dict):
                     report_content += f"**Flow & Navigation Assessment:** {flow_nav.get('assessment', 'N/A')}\n\n"

            # Handle Style specific fields
            elif key == "Style":
                analysis = section_data.get("analysis", {})
                if isinstance(analysis, dict):
                    report_content += f"**Sub-Analysis:**\n"
                    report_content += f"  - Voice & Tone: {analysis.get('voice_tone', 'N/A')}\n"
                    report_content += f"  - Clarity & Conciseness: {analysis.get('clarity_conciseness', 'N/A')}\n"
                    report_content += f"  - Action-Oriented Language: {analysis.get('action_oriented_language', 'N/A')}\n\n"

            # Common fields: Issues and Suggestions
            report_content += f"**Issues Found:**\n"
            issues = section_data.get("issues", [])
            if issues and isinstance(issues, list):
                for issue in issues:
                    report_content += f"- {issue}\n"
            else:
                report_content += "- None\n"
            report_content += "\n"

            report_content += f"**Suggestions:**\n"
            suggestions = section_data.get("suggestions", [])
            if suggestions and isinstance(suggestions, list):
                for suggestion in suggestions:
                    report_content += f"- {suggestion}\n"
            else:
                report_content += "- None\n"
            report_content += "\n"

        else:
            # Handle missing or malformed section data
            logging.warning(f"Analysis result for {key} is missing or malformed for Markdown report.")
            report_content += f"*Analysis data for this section is missing or malformed.*\n\n"
        report_content += "---\n\n"

    logging.info(f"Markdown report generated successfully for {url}.")
    return report_content

# Example usage remains the same conceptually, but the input structure to the reporter
# should now match the new detailed format produced by the updated analyzer modules.
if __name__ == '__main__':
    # Example with the NEW detailed structure
    sample_analyses_new_format = {
        "Readability": {
            "score": "Fair",
            "assessment": "Generally okay, but too much jargon for marketers.",
            "issues": ["Uses term X", "Sentence Y too complex"],
            "suggestions": ["Define X", "Split Y"]
        },
        "Structure": {
            "score": "Fair",
            "assessment": "Basic structure exists, but lacks hierarchy and clarity.",
            "counts": {"h1": 1, "h2": 3, "h3": 0, "paragraphs": 15, "lists": 2},
            "analysis": {"headings": "H2s are okay, needs H3s.", "paragraphs_lists": "Paragraphs too long, lists okay."}, 
            "flow_navigation": {"assessment": "Flow is okay, navigation poor."}, 
            "issues": ["Long paragraphs", "No H3s"],
            "suggestions": ["Break up paragraphs", "Add H3s"]
        },
        "Completeness": {
            "score": "Poor",
            "assessment": "Missing key examples and details.",
            "issues": ["No code examples", "Glossary missing"],
            "suggestions": ["Add Python example", "Create glossary"]
        },
        "Style": {
            "score": "Good",
            "assessment": "Mostly good, some minor issues.",
            "analysis": {"voice_tone": "Good", "clarity_conciseness": "Fair", "action_oriented_language": "Good"},
            "issues": ["Passive voice in section Z"],
            "suggestions": ["Rewrite Z actively"]
        }
    }
    sample_url = "https://example.com/doc_new"

    print("\n--- Generating JSON Report (New Detailed Format) --- \n")
    json_report_new = generate_report(sample_url, sample_analyses_new_format, output_format="json")
    print(json_report_new)

    print("\n--- Generating Markdown Report (New Detailed Format) ---  \n")
    markdown_report_new = generate_report(sample_url, sample_analyses_new_format, output_format="markdown")
    print(markdown_report_new)

