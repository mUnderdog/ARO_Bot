import google.generativeai as genai
from config import GEMINI_API_KEY
import os

genai.configure(api_key=GEMINI_API_KEY)

models_to_test = [
    'gemini-flash-latest',
    'gemini-pro-latest',
    'models/gemini-1.5-flash-latest', # Sometimes listed with models/ prefix
    'models/gemini-1.5-flash-001'
]

print("Testing models...")
for m_name in models_to_test:
    print(f"Testing {m_name}...", end=" ")
    try:
        model = genai.GenerativeModel(m_name)
        response = model.generate_content("Hello")
        print(f"SUCCESS! Response: {response.text.strip()[:20]}...")
        break # Found a working one!
    except Exception as e:
        print(f"FAILED: {e}")
