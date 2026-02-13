# -*- coding: utf-8 -*-
import pandas as pd
from utils.search import search_companies
from utils.researcher import research_company
from utils.writer import write_email

# Enable UTF-8 output on Windows
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open("prompts/researcher.txt", encoding='utf-8') as f:
    researcher_prompt = f.read()

with open("prompts/email_writer.txt", encoding='utf-8') as f:
    email_prompt = f.read()

query = "AI startups in Noida"
companies = search_companies(query)

print(f"\n[*] Found {len(companies)} companies to research\n")

results = []

for name in companies:
    print(f"[*] Researching: {name}")
    
    info = research_company(name, researcher_prompt)
    email = write_email(info, email_prompt)

    results.append({
        "company": name,
        "research": info,
        "email": email
    })

df = pd.DataFrame(results)
df.to_csv("data/leads.csv", index=False, encoding='utf-8')

print("\n[+] Done! leads.csv created.")
