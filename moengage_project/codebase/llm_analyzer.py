#!/usr/bin/env python
# -*- coding: utf-8 -*-
import google.generativeai as genai
import os
import logging
import time

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# --- IMPORTANT: API Key Configuration ---
# Default API key provided by user
DEFAULT_API_KEY = "AIzaSyCSD6T2I7Gk3ZEV5-hWqkT3yQgRc--P45g"
API_KEY = os.getenv("GOOGLE_API_KEY", DEFAULT_API_KEY)
model = None # Initialize model to None globally

try:
    genai.configure(api_key=API_KEY)
    # Initialize the model only AFTER successful configuration
    model = genai.GenerativeModel("gemini-2.0-flash") 
    logging.info("Gemini API configured successfully and model initialized.")
except Exception as e:
    logging.error(f"Error configuring Gemini API or initializing model: {e}")
    # Model remains None, subsequent calls will fail

def analyze_text_with_llm(prompt: str, text_content: str, max_retries=3, delay=5) -> str | None:
    """Sends text content and a specific analysis prompt to the Gemini API."""
    # Check if the model was successfully initialized
    if model is None:
        logging.error("Gemini model is not initialized. Cannot perform analysis.")
        return "Error: Gemini model not initialized. Check API key and configuration."
        
    # API Key check is implicitly handled by checking if model is initialized
    # if API_KEY == "YOUR_API_KEY": 
    #     logging.error("Cannot call Gemini API without a valid API Key.")
    #     return "Error: Gemini API Key not configured."

    full_prompt = f"""{prompt}\n\n---\nArticle Content:\n{text_content}\n---"""
    
    retries = 0
    while retries < max_retries:
        try:
            logging.info(f"Sending request to Gemini API (Attempt {retries + 1}/{max_retries})...")
            # Use the globally initialized model variable
            response = model.generate_content(full_prompt)
            
            # Check if the response has the expected text part
            if response.parts:
                analysis_result = response.text
                logging.info("Successfully received analysis from Gemini API.")
                return analysis_result
            else:
                # Handle cases where the response might be blocked or empty
                logging.warning(f"Gemini API response was empty or blocked. Safety ratings: {response.prompt_feedback}")
                block_reason = getattr(response.prompt_feedback, 'block_reason', 'Unknown')
                return f"Error: Analysis blocked by API. Reason: {block_reason}"

        except Exception as e:
            retries += 1
            logging.error(f"Error calling Gemini API: {e}. Retrying in {delay} seconds... ({retries}/{max_retries})")
            if retries >= max_retries:
                logging.error("Max retries reached. Failed to get analysis from Gemini API.")
                return f"Error: Failed to analyze text after {max_retries} attempts. Last error: {e}"
            time.sleep(delay)
            
    return None # Should theoretically not be reached

# Example usage (for testing purposes)
if __name__ == '__main__':
    # This example assumes you have set the GOOGLE_API_KEY environment variable
    if model: # Check if model was initialized successfully
        sample_text = "This is a sample document. It has some sentences. Some are short, others might be a bit longer. We aim for clarity."
        sample_prompt = "Analyze the following text for readability from the perspective of a non-technical marketer. Explain why it is readable or not, and provide specific suggestions for improvement."
        
        analysis = analyze_text_with_llm(sample_prompt, sample_text)
        
        if analysis:
            print("\n--- LLM Analysis Result ---")
            print(analysis)
        else:
            print("\n--- Failed to get LLM Analysis ---")
    else:
        print("\nPlease set the GOOGLE_API_KEY environment variable correctly to run the LLM analysis example.")

