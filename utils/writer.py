from utils.llm import ask_llm

def write_email(company_info, email_prompt):
    prompt = f"""
{email_prompt}

Company details:
{company_info}
"""
    return ask_llm(prompt)
