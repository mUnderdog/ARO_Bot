from utils.llm import ask_llm

def research_company(name, prompt_template):
    prompt = f"""
{prompt_template}

Company name: {name}
"""
    return ask_llm(prompt)
