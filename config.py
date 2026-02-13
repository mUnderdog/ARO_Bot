import os
from dotenv import load_dotenv

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GOOGLE_CSE_ID = os.getenv("GOOGLE_CSE_ID")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    print("[!] Warning: GEMINI_API_KEY not found in environment variables. LLM features will fail.")

if not GOOGLE_API_KEY or not GOOGLE_CSE_ID:
    print("[!] Warning: Google Search API keys not found. Search will use demo data.")
