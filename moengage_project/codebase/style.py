import logging
import json
from llm_analyzer import analyze_text_with_llm

# Configure logging - Corrected format string
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Updated prompt asking for sub-assessments
STYLE_GUIDELINES_PROMPT = """Analyze the following documentation article content based on these simplified style guidelines:

**Key Style Aspects:**
1.  **Voice and Tone:** Customer-focused, helpful, clear, concise? Avoid overly casual/formal.
2.  **Clarity and Conciseness:** Clear sentences? Unnecessary jargon/wordiness? Complex structures? Acronyms defined?
3.  **Action-Oriented Language:** Strong verbs? Clear guidance on actions?

**Output Requirements:**
Provide your analysis *only* as a JSON object (no surrounding text or markdown formatting) with the following exact structure:

{
  "score": "<Score>", // Overall score: Good, Fair, or Poor
  "assessment": "<Brief overall assessment of style adherence.>",
  "analysis": {
    "voice_tone": "<Assessment of voice and tone.>",
    "clarity_conciseness": "<Assessment of clarity and conciseness.>",
    "action_oriented_language": "<Assessment of action-oriented language.>"
  },
  "issues": [
    "<Specific issue 1 related to style.>",
    "<Specific issue 2 related to style.>",
    ...
  ],
  "suggestions": [
    "<Specific suggestion 1 for style improvement.>",
    "<Specific suggestion 2 for style improvement.>",
    ...
  ]
}

- **score**: Assign an overall score for style adherence: "Good", "Fair", or "Poor".
- **assessment**: Start with a brief (1-2 sentence) overall assessment.
- **analysis**: Provide brief text assessments for each of the three key style aspects.
- **issues**: List specific examples of deviations (e.g., inappropriate tone, jargon, passive voice).
- **suggestions**: Provide concrete suggestions for improvement (e.g., "Replace jargon X with simpler term Y," "Rephrase passive sentence Z actively.").

Analyze the following text:
"""

def analyze_style(article_content: str) -> dict | None:
    """Analyzes the article content against simplified style guidelines using the LLM and returns a structured dict."""
    logging.info("Starting style guidelines analysis (with sub-assessments)...")
    analysis_text = analyze_text_with_llm(STYLE_GUIDELINES_PROMPT, article_content)

    default_error_structure = {
        "score": "Error",
        "assessment": "LLM analysis failed.",
        "analysis": {
            "voice_tone": "N/A",
            "clarity_conciseness": "N/A",
            "action_oriented_language": "N/A"
        },
        "issues": [f"LLM analysis failed: {analysis_text or 'No response'}"],
        "suggestions": []
    }

    if not analysis_text or analysis_text.startswith("Error:"):
        logging.error(f"Style analysis failed or returned error: {analysis_text}")
        default_error_structure["issues"] = [f"LLM analysis failed: {analysis_text}"]
        return default_error_structure

    try:
        # Clean the response
        cleaned_text = analysis_text.strip().strip("`json\n").strip("\n```")
        analysis_data = json.loads(cleaned_text)

        # Basic validation of the new structure
        required_keys = ["score", "assessment", "analysis", "issues", "suggestions"]
        if not all(k in analysis_data for k in required_keys):
            raise ValueError(f"LLM response missing required keys. Expected: {required_keys}")
        if not isinstance(analysis_data["analysis"], dict) or not all(k in analysis_data["analysis"] for k in ["voice_tone", "clarity_conciseness", "action_oriented_language"]):
            raise ValueError("LLM response missing required keys in 'analysis'.")
        if not isinstance(analysis_data["issues"], list) or not isinstance(analysis_data["suggestions"], list):
            raise ValueError("LLM response 'issues' or 'suggestions' is not a list.")

        logging.info("Style analysis completed and parsed successfully.")
        return analysis_data
    except (json.JSONDecodeError, ValueError) as e:
        logging.error(f"Failed to parse or validate JSON response from LLM for style: {e}\nRaw response: {analysis_text}")
        default_error_structure["issues"] = [f"Failed to parse/validate LLM response: {e}"]
        default_error_structure["suggestions"] = [f"Raw LLM response: {analysis_text}"]
        return default_error_structure
    except Exception as e:
        logging.error(f"An unexpected error occurred during style analysis parsing: {e}")
        default_error_structure["issues"] = [f"Unexpected error: {e}"]
        default_error_structure["suggestions"] = [f"Raw LLM response: {analysis_text}"]
        return default_error_structure

# Example usage (for testing purposes)
if __name__ == '__main__':
    from llm_analyzer import API_KEY # Check if API key is set
    if API_KEY != "YOUR_API_KEY":
        sample_content = """
        # Utilizing the Platform
        It is recommended that users make use of the functionalities provided. In order to start, the button must be clicked.
        The system possesses capabilities for data analysis. Configuration is accomplished through the interface.
        We think you'll find this very useful for your business goals.
        """
        style_analysis = analyze_style(sample_content)
        print("\n--- Style Guidelines Analysis (Structured with Sub-Assessments) ---  \n")
        print(json.dumps(style_analysis, indent=2))
    else:
        print("\nPlease set the GOOGLE_API_KEY environment variable to run the example.")

