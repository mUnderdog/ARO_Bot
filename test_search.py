# -*- coding: utf-8 -*-
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from utils.search import search_companies

query = "AI startups in Noida"
companies = search_companies(query)

print(f"Found {len(companies)} companies:")
for i, company in enumerate(companies, 1):
    print(f"{i}. {company}")
