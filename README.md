# ARO_Bot (Automated Research & Outreach Bot)

ARO_Bot is an AI-powered tool designed to automate the process of finding specialized companies, researching them, and drafting personalized outreach emails.

## Features

- **Automated Search:** Finds companies based on a query using Google Custom Search API.
- **AI Research:** Uses Google Gemini (via `gemini-flash-latest`) to analyze each company and find key details.
- **Smart Email Drafting:** Generates personalized cold emails tailored to the specific company's work and industry.
- **CSV Export:** Saves all leads, research, and drafts into a neat CSV file.

## Setup

1.  Clone the repository:
    ```bash
    git clone https://github.com/Start-End-7/ARO_Bot
    cd ARO_Bot
    ```

2.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3.  Configure API Keys:
    - Rename `.env.example` to `.env` (or create one).
    - Add your keys:
        ```env
        GEMINI_API_KEY=your_gemini_key
        GOOGLE_API_KEY=your_google_key
        GOOGLE_CSE_ID=your_cse_id
        ```

## Usage

Run the main script:

```bash
python main.py
```

The results will be saved in `data/leads.csv`.

## Requirements

- Python 3.8+
- Google Gemini API Key
- Google Custom Search JSON API Key
