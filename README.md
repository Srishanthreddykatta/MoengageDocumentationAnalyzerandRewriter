# MoengageDocumentationAnalyzerandRewriter
# MoEngage Article Analyzer & Reviser

This project provides a Python-based toolset to automatically fetch, analyze, and revise articles from the MoEngage help documentation website (`help.moengage.com`). It leverages Large Language Models (LLMs) via the Google Generative AI API (Gemini) to perform in-depth analysis across several quality dimensions and subsequently generate an improved version of the article based on the analysis suggestions.

## Project Goal

The primary goal of this project is to automate the process of evaluating and improving the quality of technical documentation. By analyzing articles for readability, structure, completeness, and adherence to style guidelines, it provides actionable feedback. Furthermore, it attempts to automatically incorporate this feedback into a revised version of the article, streamlining the content improvement workflow.

## Features

*   **Web Content Fetching:** Uses Playwright to reliably fetch the main textual content from a given MoEngage help article URL, handling dynamic content loading.
*   **Whitespace Normalization:** Cleans the fetched text by normalizing excessive whitespace and line breaks for consistent processing.
*   **Multi-Dimensional LLM Analysis:** Performs analysis using Google's Gemini model across four key areas:
    *   **Readability:** Assesses clarity, conciseness, and suitability for the target audience (marketers).
    *   **Structure & Flow:** Evaluates logical organization, headings, lists, and overall flow.
    *   **Completeness:** Checks for sufficient detail, examples, and coverage of the topic.
    *   **Style Guidelines:** Assesses adherence to predefined style conventions (tone, voice, formatting).
*   **Detailed Reporting:** Generates comprehensive analysis reports in two formats:
    *   **Markdown (`.md`):** Human-readable report summarizing scores, findings, and suggestions for each analysis dimension.
    *   **JSON (`.json`):** Machine-readable report containing structured analysis data, scores, and suggestions.
*   **Automated Revision:** Utilizes the analysis suggestions (from the JSON report) and the original article content to prompt the LLM to generate a revised version of the article.
*   **Content Preservation:** The revision process is specifically instructed to preserve original hyperlinks and Markdown table structures verbatim to maintain critical information and formatting.
*   **Dual Format Revised Output:** Saves the automatically revised article in both plain text (`.txt`) and Markdown (`.md`) formats.
*   **Command-Line Interface:** Easy to run via the command line, accepting the target URL and an optional output directory.
*   **Environment Variable Configuration:** Requires a Google API key to be configured via the `GOOGLE_API_KEY` environment variable.

## Technology Stack

*   **Language:** Python 3.11
*   **Web Scraping:** Playwright
*   **LLM Interaction:** Google Generative AI SDK (for Gemini Pro)
*   **Core Libraries:** `argparse`, `os`, `logging`, `json`, `re`, `urllib`

## Project Structure

```
.
├── codebase/
│   ├── main.py             # Main script to orchestrate the workflow
│   ├── scraper.py          # Fetches and cleans article content
│   ├── llm_analyzer.py     # Handles interaction with the Gemini API
│   ├── readability.py      # Logic and prompt for readability analysis
│   ├── structure.py        # Logic and prompt for structure analysis
│   ├── completeness.py     # Logic and prompt for completeness analysis
│   ├── style.py            # Logic and prompt for style analysis
│   ├── reporter.py         # Generates Markdown and JSON reports
│   ├── revision_agent.py   # Generates revised article using LLM
│   ├── requirements.txt    # Python package dependencies
│   ├── test_output.json    # Example output file (may be outdated)
│   └── pasted_content.txt  # User-provided text (likely for testing)
│   └── __pycache__/        # Python bytecode cache (auto-generated)
├── output/                 # Default directory for generated reports and revisions
│   ├── [article_id]_analysis.json
│   ├── [article_id]_analysis.md
│   ├── [article_id]_revised.txt
│   └── [article_id]_revised.md
└── README.md               # This file
```

## Setup

1.  **Clone the Repository:**
    ```bash
    git clone <your-repository-url>
    cd <repository-directory>
    ```
2.  **Install Dependencies:**
    Make sure you have Python 3.11 or later installed.
    ```bash
    pip install -r codebase/requirements.txt
    ```
3.  **Install Playwright Browsers:**
    Playwright needs browser binaries to function.
    ```bash
    playwright install
    ```
4.  **Set Google API Key:**
    This project requires access to the Google Generative AI API (Gemini). Obtain an API key from [Google AI Studio](https://aistudio.google.com/app/apikey) and set it as an environment variable.
    *   **Linux/macOS:**
        ```bash
        export GOOGLE_API_KEY=\'YOUR_API_KEY\'
        ```
    *   **Windows (Command Prompt):**
        ```cmd
        set GOOGLE_API_KEY=YOUR_API_KEY
        ```
    *   **Windows (PowerShell):**
        ```powershell
        $env:GOOGLE_API_KEY=\'YOUR_API_KEY\'
        ```
    Replace `YOUR_API_KEY` with your actual key.

## Usage

Run the main script from the command line, providing the URL of the MoEngage help article you want to process.

```bash
cd codebase # Navigate into the codebase directory if needed

# Example:
python main.py "https://help.moengage.com/hc/en-us/articles/31633492991124-Overview-Data-Management"

# Specify a different output directory:
python main.py "<article_url>" -o /path/to/your/output/folder
```

The script will:
1.  Fetch the content from the URL.
2.  Perform the analyses.
3.  Generate the JSON and Markdown analysis reports in the specified output directory (defaults to `../output/` relative to the script).
4.  Generate the revised article (`.txt` and `.md`) based on the analysis and save it to the output directory.

Log messages will be printed to the console indicating the progress.

## How it Works

1.  **Scraping (`scraper.py`):** Playwright launches a headless browser, navigates to the URL, identifies the main article content container (using selectors like `div.article-body` or fallbacks like `article`), extracts the text, and normalizes whitespace.
2.  **Analysis (`readability.py`, `structure.py`, etc. + `llm_analyzer.py`):** The normalized text is sent to the Gemini API via `llm_analyzer.py`, using specific prompts defined in each analysis module (`readability.py`, etc.) to evaluate different quality aspects.
3.  **Reporting (`reporter.py`):** The structured results from the LLM analyses are compiled into user-friendly Markdown and structured JSON reports.
4.  **Revision (`revision_agent.py`):** The original (normalized) article content and the suggestions from the JSON report are combined into a detailed prompt for the LLM. This prompt instructs the LLM to revise the text based *only* on the suggestions while strictly preserving original links and Markdown tables verbatim. The resulting revised text is saved.
5.  **Orchestration (`main.py`):** This script ties everything together, handling argument parsing, calling the scraper, analysis modules, reporter, and revision agent in sequence, and managing file I/O.

## Potential Improvements

*   **Error Handling:** More robust error handling for network issues, LLM API errors, and unexpected website structures.
*   **Configuration File:** Move settings like API keys (though env var is good practice), prompts, or selectors to a configuration file (e.g., YAML, JSON).
*   **Batch Processing:** Add functionality to process multiple URLs from a list or file.
*   **Diff Generation:** Show a diff between the original and revised articles for easier review.
*   **Testing:** Implement unit and integration tests for better reliability.

