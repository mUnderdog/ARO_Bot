import time
import os
import openai
from config import OPENAI_API_KEY

def ask_llm(prompt: str, retries: int = 2) -> str:
    """
    Query the OpenAI GPT model.
    Handles quota errors with a brief retry and clear error messages.
    """
    if not OPENAI_API_KEY:
        return "Error: OPENAI_API_KEY is missing from .env"

    client = openai.OpenAI(api_key=OPENAI_API_KEY)

    for attempt in range(retries + 1):
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
            )
            return response.choices[0].message.content

        except openai.RateLimitError as e:
            msg = str(e).lower()
            if "insufficient_quota" in msg or "quota exceeded" in msg:
                return (
                    "⚠️ OpenAI API quota exhausted.\n\n"
                    "You have exceeded your current quota or your billing balance is exhausted. "
                    "Please check your plan and billing details at https://platform.openai.com/account/billing"
                )
            if attempt < retries:
                wait = 20 * (attempt + 1)
                time.sleep(wait)
                continue
            return f"⚠️ OpenAI API rate limit hit after {retries} retries. Try again in a minute."

        except openai.AuthenticationError as e:
            return (
                "⚠️ OpenAI API authentication failed.\n\n"
                "Check that OPENAI_API_KEY in your .env is correct and active."
            )
        except openai.APIError as e:
            return f"Error querying LLM API: {str(e)}"
        except Exception as e:
            return f"Unexpected LLM error: {str(e)}"
