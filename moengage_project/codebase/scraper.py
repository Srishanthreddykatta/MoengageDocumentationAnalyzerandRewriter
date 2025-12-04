#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import time
import re # Import regex module
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError

# Corrected logging format string
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def normalize_whitespace(text: str) -> str:
    """Cleans and normalizes whitespace in the extracted text."""
    if not text:
        return ""
    # Replace multiple spaces/tabs with a single space
    text = re.sub(r'[ \t]+', ' ', text)
    # Replace multiple newlines with max two newlines (to preserve paragraph breaks)
    text = re.sub(r'\n{3,}', '\n\n', text)
    # Strip leading/trailing whitespace from each line and handle paragraph spacing
    lines = text.split('\n')
    cleaned_lines = []
    for i, line in enumerate(lines):
        stripped_line = line.strip()
        if stripped_line: # Keep non-empty lines
            cleaned_lines.append(stripped_line)
        elif i > 0 and cleaned_lines and cleaned_lines[-1]: # Keep a single blank line for paragraph breaks
            cleaned_lines.append("") # Add a single blank line
            
    # Remove any leading/trailing blank lines potentially added
    while cleaned_lines and not cleaned_lines[0]:
        cleaned_lines.pop(0)
    while cleaned_lines and not cleaned_lines[-1]:
        cleaned_lines.pop()
        
    # Join lines back
    text = '\n'.join(cleaned_lines)
    # Final strip of leading/trailing whitespace from the whole text
    return text.strip()

def fetch_article_content(url: str) -> str | None:
    """Fetches and extracts the main article content from a URL using Playwright."""
    pw = None
    browser = None
    try:
        pw = sync_playwright().start()
        browser = pw.chromium.launch(headless=True)
        page = browser.new_page(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        )
        
        logging.info(f"Navigating to {url} using Playwright...")
        page.goto(url, timeout=30000) # 30 second timeout for navigation

        # Try multiple selectors to work with different website structures
        content_selector = "div.article-body"
        fallback_selectors = [
            "article",
            "main",
            "[role='main']",
            ".content",
            ".post-content",
            ".entry-content",
            "#content",
            ".article-content",
            ".documentation-content",
            "body"  # Last resort
        ]

        article_body_element = None
        used_selector = None
        
        # Try primary selector first
        try:
            page.wait_for_selector(content_selector, timeout=10000)
            article_body_element = page.locator(content_selector).first
            used_selector = content_selector
            logging.info(f"Found content using primary selector: {content_selector}")
        except PlaywrightTimeoutError:
            logging.warning(f"Primary selector {content_selector} not found, trying fallback selectors...")
            # Try all fallback selectors
            for selector in fallback_selectors:
                try:
                    page.wait_for_selector(selector, timeout=5000)
                    article_body_element = page.locator(selector).first
                    used_selector = selector
                    logging.info(f"Found content using fallback selector: {selector}")
                    break
                except PlaywrightTimeoutError:
                    continue
            
            if article_body_element is None:
                logging.error(f"Could not find main article body using any selector in {url}.")
                return None

        text_content = article_body_element.text_content()
        
        if text_content:
            logging.info(f"Successfully extracted content from {url} using Playwright")
            # Normalize whitespace before returning
            normalized_content = normalize_whitespace(text_content)
            logging.info("Applied whitespace normalization to extracted content.")
            return normalized_content
        else:
            logging.warning(f"Located article body for {url}, but it contained no text.")
            return None

    except PlaywrightTimeoutError as e:
        logging.error(f"Playwright timeout error accessing {url}: {e}")
        return None
    except Exception as e:
        logging.error(f"Error processing URL {url} with Playwright: {e}")
        return None
    finally:
        if browser:
            browser.close()
        if pw:
            pw.stop()

# Example usage (for testing purposes)
if __name__ == '__main__':
    test_url = "https://help.moengage.com/hc/en-us/articles/33436161901332-Sign-Up-with-MoEngage-or-Create-a-New-Account-in-MoEngage#h_01HCF71DEQY09CG9KXW1AYQ73F"
    
    print(f"Attempting to fetch content from: {test_url}")
    content = fetch_article_content(test_url)
    
    if content:
        print(f"\n--- Content fetched successfully (first 500 chars) ---")
        print(content[:500] + "...")
        # Save normalized content for inspection
        try:
            with open("/home/ubuntu/normalized_test_output.txt", "w", encoding="utf-8") as f:
                f.write(content)
            print("\nNormalized content saved to /home/ubuntu/normalized_test_output.txt for inspection.")
        except Exception as e:
            print(f"\nError saving normalized content: {e}")
    else:
        print("\n--- Failed to fetch content ---")

