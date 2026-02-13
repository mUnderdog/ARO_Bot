import pandas as pd
from utils.search import search_companies
from utils.researcher import research_company
from utils.writer import write_email

with open("prompts/researcher.txt") as f:
    researcher_prompt = f.read()

with open("prompts/email_writer.txt") as f:
    email_prompt = f.read()

query = "AI startups in Noida"
companies = search_companies(query)

results = []

for name in companies:
    print(f"\n🔍 Researching: {name}")
    
    info = research_company(name, researcher_prompt)
    email = write_email(info, email_prompt)

    results.append({
        "company": name,
        "research": info,
        "email": email
    })

df = pd.DataFrame(results)
df.to_csv("data/leads.csv", index=False)

print("\n✅ Done! leads.csv created.")
