from llm_analyzer import analyze_text_with_llm
import logging
import json

# Corrected logging format string
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Updated prompt asking for assessment first
READABILITY_PROMPT = """
Analyze the following documentation article content strictly from the perspective of a **non-technical business user or general audience**.

**Assessment Criteria:**
1.  **Clarity:** Is the language clear, simple, and free of overly technical jargon?
2.  **Engagement:** Is the text engaging and easy to follow for this audience?
3.  **Actionability:** Can this audience easily understand the core concepts and benefits?

**Output Requirements:**
Provide your analysis *only* as a JSON object (no surrounding text or markdown formatting) with the following exact structure:

{
  "score": "<Score>", // Overall score: Good, Fair, or Poor
  "assessment": "<Brief overall assessment of readability for a non-technical audience.>",
  "issues": [
    "<Specific issue 1 related to readability (e.g., jargon, complexity).>",
    "<Specific issue 2 related to readability.>",
    ...
  ],
  "suggestions": [
    "<Specific suggestion 1 for readability improvement.>",
    "<Specific suggestion 2 for readability improvement.>",
    ...
  ]
}

- **score**: Assign an overall score for readability: "Good", "Fair", or "Poor".
- **assessment**: Start with a brief (1-2 sentence) overall assessment explaining *why* it is or isn't readable for this audience.
- **issues**: List specific sentences, phrases, or sections that are too technical, unclear, or disengaging.
- **suggestions**: Provide concrete, actionable suggestions for how to rephrase or simplify.

Analyze the following text:
"""

def analyze_readability(article_content: str) -> dict | None:
    """Analyzes the readability for a non-technical marketer using the LLM and returns a structured dict."""
    logging.info("Starting readability analysis (with assessment)...")
    analysis_text = analyze_text_with_llm(READABILITY_PROMPT, article_content)

    default_error_structure = {
        "score": "Error",
        "assessment": "LLM analysis failed.",
        "issues": [f"LLM analysis failed: {analysis_text or 'No response'}"],
        "suggestions": []
    }

    if not analysis_text or analysis_text.startswith("Error:"):
        logging.error(f"Readability analysis failed or returned error: {analysis_text}")
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

        logging.info("Readability analysis completed and parsed successfully.")
        return analysis_data
    except (json.JSONDecodeError, ValueError) as e:
        logging.error(f"Failed to parse or validate JSON response from LLM for readability: {e}\nRaw response: {analysis_text}")
        default_error_structure["issues"] = [f"Failed to parse/validate LLM response: {e}"]
        default_error_structure["suggestions"] = [f"Raw LLM response: {analysis_text}"]
        return default_error_structure
    except Exception as e:
        logging.error(f"An unexpected error occurred during readability analysis parsing: {e}")
        default_error_structure["issues"] = [f"Unexpected error: {e}"]
        default_error_structure["suggestions"] = [f"Raw LLM response: {analysis_text}"]
        return default_error_structure

# Example usage (for testing purposes)
if __name__ == '__main__':
    from llm_analyzer import API_KEY # Check if API key is set
    if API_KEY != "YOUR_API_KEY":
        sample_content = """
        Welcome to Advanced Segmentation Setup.
        To begin, you must first instantiate the primary data ingestion pipeline by configuring the appropriate Kafka topic ACLs. Ensure that the replication factor is set to 3 for optimal fault tolerance. 
        Marketers will appreciate the ability to target users based on granular attributes. This powerful feature allows for personalized campaigns.
        Subsequently, leverage the REST API to push user profile updates. Use the PATCH method for partial updates to avoid overwriting existing data fields. The endpoint requires OAuth2 authentication.
        """
        readability_analysis = analyze_readability(sample_content)
        print("\n--- Readability Analysis (Structured with Assessment) ---  \n")
        print(json.dumps(readability_analysis, indent=2))
    else:
        print("\nPlease set the GOOGLE_API_KEY environment variable to run the example.")

