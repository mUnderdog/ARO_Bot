import time
from google import genai
from google.genai import errors as genai_errors
from config import GEMINI_API_KEY

def ask_llm(prompt: str, retries: int = 2) -> str:
    """
    Query the Google Gemini model using the new google-genai SDK.
    Handles quota errors with a brief retry and clear error messages.
    """
    if not GEMINI_API_KEY:
        return "Error: GEMINI_API_KEY is missing from .env"

    client = genai.Client(api_key=GEMINI_API_KEY)

    for attempt in range(retries + 1):
        try:
            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=prompt,
            )
            return response.text

        except genai_errors.ClientError as e:
            code = e.code if hasattr(e, "code") else 0
            msg  = str(e)

            if code == 429:
                # Daily quota exhausted — no point retrying
                if "generate_content_free_tier" in msg and "limit: 0" in msg:
                    return (
                        "⚠️ Gemini API daily quota exhausted.\n\n"
                        "The free-tier daily request limit for this API key has been reached. "
                        "Please wait until tomorrow for the quota to reset, or upgrade your "
                        "Google AI Studio plan at https://ai.google.dev/gemini-api/docs/rate-limits"
                    )
                # Minute-level throttle — wait and retry
                if attempt < retries:
                    wait = 20 * (attempt + 1)
                    time.sleep(wait)
                    continue
                return f"⚠️ Gemini API rate limit hit after {retries} retries. Try again in a minute."

            if code == 401 or code == 403:
                return (
                    "⚠️ Gemini API authentication failed.\n\n"
                    "Check that GEMINI_API_KEY in your .env is correct and active."
                )

            return f"Error querying LLM ({code}): {str(e)}"

        except Exception as e:
            return f"Unexpected LLM error: {str(e)}"
