# -*- coding: utf-8 -*-
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import requests

# Test Ollama connection
try:
    response = requests.get("http://localhost:11434/api/tags", timeout=5)
    if response.status_code == 200:
        print("[+] Ollama server is running")
        models = response.json().get("models", [])
        print(f"[*] Available models: {len(models)}")
        for model in models:
            print(f"  - {model.get('name', 'unknown')}")
    else:
        print("[!] Ollama server returned unexpected status")
except Exception as e:
    print(f"[!] Cannot connect to Ollama: {e}")
    print("[!] Make sure Ollama is running with: ollama serve")
