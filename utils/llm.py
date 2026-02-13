import google.generativeai as genai
from config import GEMINI_API_KEY
import os

# Configure the Gemini API
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
else:
    print("Warning: internal LLM configuration skipped due to missing API key.")

def ask_llm(prompt):
    """
    Query the Google Gemini model.
    """
    if not GEMINI_API_KEY:
        return "Error: configured GEMINI_API_KEY is missing."

    try:
        model = genai.GenerativeModel('gemini-flash-latest') # Verified working model alias
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error querying LLM: {str(e)}"
