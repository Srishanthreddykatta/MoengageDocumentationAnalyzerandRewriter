from llm_analyzer import analyze_text_with_llm
import logging
import json
import re # Import re for potential counting

# Corrected logging format string
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Updated prompt asking for counts and specific structure analysis
STRUCTURE_FLOW_PROMPT = """
Analyze the structure and logical flow of the following documentation article content.

**Assessment Criteria:**
1.  **Counts:** Count the number of H1, H2, H3 headings, paragraphs, and lists (bulleted or numbered).
2.  **Structure Analysis:** Based on the counts and content, assess the effectiveness of headings, paragraph length, and list usage.
3.  **Logical Flow & Navigability:** Assess if the information progresses logically and if it's easy to scan and find information.

**Output Requirements:**
Provide your analysis *only* as a JSON object (no surrounding text or markdown formatting) with the following exact structure:

{
  "score": "<Score>", // Overall score: Good, Fair, or Poor
  "assessment": "<Brief overall assessment of structure and flow.>",
  "counts": {
    "h1": <count>,
    "h2": <count>,
    "h3": <count>,
    "paragraphs": <count>,
    "lists": <count>
  },
  "analysis": {
    "headings": "<Analysis of heading usage effectiveness.>",
    "paragraphs_lists": "<Analysis of paragraph length and list usage.>"
  },
  "flow_navigation": {
    "assessment": "<Assessment of logical flow and navigability.>"
  },
  "issues": [
    "<Specific issue 1 related to structure/flow.>",
    "<Specific issue 2 related to structure/flow.>",
    ...
  ],
  "suggestions": [
    "<Specific suggestion 1 for structure/flow improvement.>",
    "<Specific suggestion 2 for structure/flow improvement.>",
    ...
  ]
}

- **score**: Assign an overall score for structure/flow: "Good", "Fair", or "Poor".
- **assessment**: Start with a brief (1-2 sentence) overall assessment.
- **counts**: Provide numerical counts for the specified elements.
- **analysis**: Provide brief text analysis for headings and paragraphs/lists.
- **flow_navigation**: Provide a brief text assessment of flow and navigation.
- **issues**: List specific problems identified.
- **suggestions**: Provide concrete, actionable suggestions for improvement.

Analyze the following text:
"""

def count_elements(text: str) -> dict:
    """Basic counting of elements using regex (as a fallback or supplement)."""
    # Note: These counts might be inaccurate for complex HTML/Markdown structures
    # It's better if the LLM provides the counts directly.
    counts = {
        "h1": len(re.findall(r"^#\s+", text, re.MULTILINE)),
        "h2": len(re.findall(r"^##\s+", text, re.MULTILINE)),
        "h3": len(re.findall(r"^###\s+", text, re.MULTILINE)),
        # Paragraph count is tricky; split by double newline, filter empty
        "paragraphs": len([p for p in text.split("\n\n") if p.strip() and not p.strip().startswith(('#', '*', '-'))]),
        "lists": len(re.findall(r"^\s*[*\-+]\s+|^\s*\d+\.\s+", text, re.MULTILINE))
    }
    return counts

def analyze_structure(article_content: str) -> dict | None:
    """Analyzes the structure and flow using the LLM and returns a structured dict."""
    logging.info("Starting structure and flow analysis (with counts)...")
    analysis_text = analyze_text_with_llm(STRUCTURE_FLOW_PROMPT, article_content)

    default_error_structure = {
            "score": "Error",
            "assessment": "LLM analysis failed.",
            "counts": {"h1": 0, "h2": 0, "h3": 0, "paragraphs": 0, "lists": 0},
            "analysis": {"headings": "N/A", "paragraphs_lists": "N/A"},
            "flow_navigation": {"assessment": "N/A"},
            "issues": [f"LLM analysis failed: {analysis_text or 'No response'}"],
            "suggestions": []
        }

    if not analysis_text or analysis_text.startswith("Error:"):
        logging.error(f"Structure analysis failed or returned error: {analysis_text}")
        default_error_structure["issues"] = [f"LLM analysis failed: {analysis_text}"]
        return default_error_structure

    try:
        # Clean the response
        cleaned_text = analysis_text.strip().strip("`json\n").strip("\n```")
        analysis_data = json.loads(cleaned_text)

        # Basic validation of the new structure
        required_keys = ["score", "assessment", "counts", "analysis", "flow_navigation", "issues", "suggestions"]
        if not all(k in analysis_data for k in required_keys):
             raise ValueError(f"LLM response missing required keys. Expected: {required_keys}")
        if not isinstance(analysis_data["counts"], dict) or not all(k in analysis_data["counts"] for k in ["h1", "h2", "h3", "paragraphs", "lists"]):
             raise ValueError("LLM response missing required keys in 'counts'.")
        if not isinstance(analysis_data["analysis"], dict) or not all(k in analysis_data["analysis"] for k in ["headings", "paragraphs_lists"]):
             raise ValueError("LLM response missing required keys in 'analysis'.")
        if not isinstance(analysis_data["flow_navigation"], dict) or "assessment" not in analysis_data["flow_navigation"]:
             raise ValueError("LLM response missing required keys in 'flow_navigation'.")
        if not isinstance(analysis_data["issues"], list) or not isinstance(analysis_data["suggestions"], list):
             raise ValueError("LLM response 'issues' or 'suggestions' is not a list.")

        logging.info("Structure analysis completed and parsed successfully.")
        return analysis_data
    except (json.JSONDecodeError, ValueError) as e:
        logging.error(f"Failed to parse or validate JSON response from LLM for structure: {e}\nRaw response: {analysis_text}")
        # Try to salvage counts if parsing failed?
        # counts_fallback = count_elements(article_content)
        # default_error_structure["counts"] = counts_fallback
        default_error_structure["issues"] = [f"Failed to parse/validate LLM response: {e}"]
        default_error_structure["suggestions"] = [f"Raw LLM response: {analysis_text}"]
        return default_error_structure
    except Exception as e:
        logging.error(f"An unexpected error occurred during structure analysis parsing: {e}")
        default_error_structure["issues"] = [f"Unexpected error: {e}"]
        default_error_structure["suggestions"] = [f"Raw LLM response: {analysis_text}"]
        return default_error_structure

# Example usage (for testing purposes)
if __name__ == '__main__':
    from llm_analyzer import API_KEY # Check if API key is set
    if API_KEY != "YOUR_API_KEY":
        sample_content = """
# Getting Started
Welcome to our platform. This guide helps you begin.

This is the first paragraph.

## Initial Setup
First, create an account. Then, verify your email. After that you need to configure your profile settings which involves uploading a picture and setting your preferences. Finally, you can create your first project.

* Step 1
* Step 2

Another paragraph here.

### Sub Setup
More details.

## Next Steps
Explore the dashboard. Read the tutorials. Contact support if needed.

1. Point one
2. Point two
        """
        structure_analysis = analyze_structure(sample_content)
        print("\n--- Structure and Flow Analysis (Structured with Counts) ---  \n")
        print(json.dumps(structure_analysis, indent=2))
    else:
        print("\nPlease set the GOOGLE_API_KEY environment variable to run the example.")

