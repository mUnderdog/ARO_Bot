import time
import os
import openai
from config import GROQ_API_KEY

def ask_llm(prompt: str, retries: int = 2) -> str:
    """
    Query the Groq Llama 3 model via the OpenAI SDK wrapper.
    Handles quota errors with a brief retry and clear error messages.
    """
    if not GROQ_API_KEY:
        return "Error: GROQ_API_KEY is missing from .env"

    client = openai.OpenAI(
        api_key=GROQ_API_KEY,
        base_url="https://api.groq.com/openai/v1"
    )

    for attempt in range(retries + 1):
        try:
            response = client.chat.completions.create(
                model="llama3-8b-8192",
                messages=[{"role": "user", "content": prompt}],
            )
            return response.choices[0].message.content

        except openai.RateLimitError as e:
            if attempt < retries:
                wait = 20 * (attempt + 1)
                time.sleep(wait)
                continue
            return f"⚠️ Groq API rate limit hit after {retries} retries. Try again in a minute."

        except openai.AuthenticationError as e:
            return (
                "⚠️ Groq API authentication failed.\n\n"
                "Check that GROQ_API_KEY in your .env is correct and active."
            )
        except openai.APIError as e:
            return f"Error querying LLM API: {str(e)}"
        except Exception as e:
            return f"Unexpected LLM error: {str(e)}"
