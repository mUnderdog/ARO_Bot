import requests
from config import GOOGLE_API_KEY, GOOGLE_CSE_ID

def search_companies(query):
    """
    Search for companies using Google Custom Search API.
    Falls back to a demo list if API keys are not configured.
    """
    
    # Check if API keys are configured
    if not GOOGLE_API_KEY or not GOOGLE_CSE_ID:
        print("[!] Warning: Google API keys not fully configured. Using demo data.")
        return get_demo_companies()
    
    try:
        url = "https://www.googleapis.com/customsearch/v1"
        params = {
            "key": GOOGLE_API_KEY,
            "cx": GOOGLE_CSE_ID,
            "q": query,
            "num": 5
        }
        
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        companies = []
        
        if "items" in data:
            for item in data["items"]:
                # Extract company name from title
                title = item.get("title", "")
                # Clean up the title (remove common suffixes)
                company_name = title.split(" - ")[0].split(" | ")[0].strip()
                if company_name:
                    companies.append(company_name)
        
        if not companies:
            print("[!] No results found. Using demo data.")
            return get_demo_companies()
            
        return companies
        
    except Exception as e:
        print(f"[!] Search error: {e}. Using demo data.")
        return get_demo_companies()


def get_demo_companies():
    """
    Returns a list of demo AI/tech companies for testing.
    Replace this with real search results once API is configured.
    """
    return [
        "TechAhead",
        "Successive Digital",
        "Appinventiv",
        "Emizentech",
        "Appsierra"
    ]
