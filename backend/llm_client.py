# backend/llm_client.py
# Robust Gemini integration: loads .env, retries, prompt-size guard, and fallback.

from dotenv import load_dotenv
import os
import time
import textwrap

load_dotenv()  # read .env

GEMINI_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL_NAME = os.getenv("GEMINI_MODEL_NAME", "gemini-1.5-flash")
MAX_PROMPT_CHARS = 30000
RETRY_COUNT = 3
RETRY_BASE_DELAY = 1.0  # seconds

# optional import of google generative ai
try:
    import google.generativeai as genai
    HAS_GENAI = True
except Exception:
    genai = None
    HAS_GENAI = False

def _call_gemini_safe(prompt: str) -> str:
    """Call Gemini with retries and clear errors."""
    if not HAS_GENAI:
        raise RuntimeError("google.generativeai not installed in the current environment.")
    if not GEMINI_KEY:
        raise RuntimeError("GEMINI_API_KEY not set. Add it to .env or export before running.")
    if len(prompt) > MAX_PROMPT_CHARS:
        raise RuntimeError(f"Prompt too long ({len(prompt)} chars) — truncate or chunk your context.")
    genai.configure(api_key=GEMINI_KEY)
    for attempt in range(1, RETRY_COUNT + 1):
        try:
            model = genai.GenerativeModel(GEMINI_MODEL_NAME)
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            if attempt == RETRY_COUNT:
                raise RuntimeError(f"Gemini API failed after {RETRY_COUNT} attempts: {e}")
            time.sleep(RETRY_BASE_DELAY * (2 ** (attempt - 1)))
    raise RuntimeError("Unexpected Gemini call failure.")

def generate_test_cases(context: str, user_query: str) -> str:
    prompt = textwrap.dedent(f"""
    You are given context and a user query. Produce clear, bounded test cases grounded in the context.
    Output a numbered markdown list with IDs, preconditions, steps, test data, and expected results.

    CONTEXT:
    {context}

    USER QUERY:
    {user_query}

    Return only the test cases in markdown format.
    """)
    try:
        return _call_gemini_safe(prompt)
    except Exception as e:
        # fallback deterministic response so UI remains usable
        return ("### (fallback) Test cases\n\n"
                "- Test Case 1: Fill in required fields and submit. Expect success.\n"
                "- Test Case 2: Leave required field blank and submit. Expect validation error.\n"
                f"\n\n[LLM unavailable or error: {e}]")

def generate_selenium_script(context: str, test_case_text: str, html_source: str) -> str:
    # keep the prompt relatively small: include an abbreviated context and a portion of HTML
    prompt = textwrap.dedent(f"""
    You are to write a runnable Python Selenium script for the following single test case.
    Use realistic selectors present in the HTML when possible. If you cannot find exact selectors,
    include comments indicating which selectors to replace.

    TEST CASE:
    {test_case_text}

    SHORT CONTEXT:
    {context[:8000]}

    PARTIAL HTML (for reference; truncated):
    {html_source[:16000]}

    Output ONLY the Python Selenium script (no explanation). Use chrome webdriver and common waits.
    """)
    try:
        return _call_gemini_safe(prompt)
    except Exception as e:
        # graceful fallback to a safe skeleton that uses data URL loading
        safe_html = html_source.replace('"""', '\\"""')
        return f'''# Fallback Selenium script (LLM unavailable: {e})
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

driver = webdriver.Chrome()
driver.get("data:text/html;charset=utf-8," + """{safe_html}""")
time.sleep(1)

# Replace selectors below with real ids/classes from your page
try:
    # Example: apply discount if elements present
    el = driver.find_element(By.ID, "discount-code")
    el.send_keys("DISC50")
    driver.find_element(By.ID, "apply-discount").click()
    time.sleep(1)
except Exception as ie:
    print("Could not interact with expected elements; update selectors:", ie)

print("Fallback script completed")
driver.quit()
'''
