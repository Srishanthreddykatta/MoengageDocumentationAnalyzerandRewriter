from llm_analyzer import analyze_text_with_llm
import logging
import json

# Corrected logging format string
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Updated prompt asking for assessment first
COMPLETENESS_EXAMPLES_PROMPT = """
Analyze the completeness and quality of examples in the following documentation article content.

**Assessment Criteria:**
1.  **Completeness:** Does the article provide enough detail to understand/implement the feature? Are there information gaps?
2.  **Examples:** Are there sufficient, clear, relevant examples (e.g., code, UI, scenarios)?
3.  **Practicality:** Does it cover common use cases or potential issues?

**Output Requirements:**
Provide your analysis *only* as a JSON object (no surrounding text or markdown formatting) with the following exact structure:

{
  "score": "<Score>", // Overall score: Good, Fair, or Poor
  "assessment": "<Brief overall assessment of completeness and examples.>",
  "issues": [
    "<Specific issue 1 related to completeness/examples.>",
    "<Specific issue 2 related to completeness/examples.>",
    ...
  ],
  "suggestions": [
    "<Specific suggestion 1 for completeness/examples improvement.>",
    "<Specific suggestion 2 for completeness/examples improvement.>",
    ...
  ]
}

- **score**: Assign an overall score for completeness/examples: "Good", "Fair", or "Poor".
- **assessment**: Start with a brief (1-2 sentence) overall assessment.
- **issues**: List specific gaps in information, missing/unclear examples, or lack of practical details.
- **suggestions**: Provide concrete suggestions, like "Add a table detailing rate limits," "Include screenshots of the UI at key steps," "Add a troubleshooting section."

Analyze the following text:
"""

def analyze_completeness(article_content: str) -> dict | None:
    """Analyzes completeness and examples using the LLM and returns a structured dict."""
    logging.info("Starting completeness and examples analysis (with assessment)...")
    analysis_text = analyze_text_with_llm(COMPLETENESS_EXAMPLES_PROMPT, article_content)

    default_error_structure = {
        "score": "Error",
        "assessment": "LLM analysis failed.",
        "issues": [f"LLM analysis failed: {analysis_text or 'No response'}"],
        "suggestions": []
    }

    if not analysis_text or analysis_text.startswith("Error:"):
        logging.error(f"Completeness analysis failed or returned error: {analysis_text}")
        default_error_structure["issues"] = [f"LLM analysis failed: {analysis_text}"]
        return default_error_structure

    try:
        # Clean the response
        cleaned_text = analysis_text.strip().strip("`json\n").strip("\n```")
        analysis_data = json.loads(cleaned_text)

        # Basic validation of the new structure
        required_keys = ["score", "assessment", "issues", "suggestions"]
        if not all(k in analysis_data for k in required_keys):
            raise ValueError(f"LLM response missing required keys. Expected: {required_keys}")
        if not isinstance(analysis_data["issues"], list) or not isinstance(analysis_data["suggestions"], list):
            raise ValueError("LLM response 'issues' or 'suggestions' is not a list.")

        logging.info("Completeness analysis completed and parsed successfully.")
        return analysis_data
    except (json.JSONDecodeError, ValueError) as e:
        logging.error(f"Failed to parse or validate JSON response from LLM for completeness: {e}\nRaw response: {analysis_text}")
        default_error_structure["issues"] = [f"Failed to parse/validate LLM response: {e}"]
        default_error_structure["suggestions"] = [f"Raw LLM response: {analysis_text}"]
        return default_error_structure
    except Exception as e:
        logging.error(f"An unexpected error occurred during completeness analysis parsing: {e}")
        default_error_structure["issues"] = [f"Unexpected error: {e}"]
        default_error_structure["suggestions"] = [f"Raw LLM response: {analysis_text}"]
        return default_error_structure

# Example usage (for testing purposes)
if __name__ == '__main__':
    from llm_analyzer import API_KEY # Check if API key is set
    if API_KEY != "YOUR_API_KEY":
        sample_content = """
        # Feature X Setup
        To use Feature X, simply enable it in your settings.
        ## How it Works
        Feature X automatically analyzes user data.
        ## Benefits
        It provides insights.
        """
        completeness_analysis = analyze_completeness(sample_content)
        print("\n--- Completeness and Examples Analysis (Structured with Assessment) ---  \n")
        print(json.dumps(completeness_analysis, indent=2))
    else:
        print("\nPlease set the GOOGLE_API_KEY environment variable to run the example.")

