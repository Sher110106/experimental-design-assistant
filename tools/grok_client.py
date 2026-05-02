"""LLM API client for structured calls (Groq-compatible)."""
import json
import time
import requests
from config import LLM_API_KEY, LLM_BASE_URL, DEFAULT_MODEL


def call_grok(
    system_prompt: str,
    user_prompt: str,
    model: str = DEFAULT_MODEL,
    temperature: float = 0.2,
    max_retries: int = 3,
) -> str:
    """Call LLM API and return the response text."""
    headers = {
        "Authorization": f"Bearer {LLM_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        "temperature": temperature,
    }

    for attempt in range(max_retries):
        try:
            response = requests.post(
                f"{LLM_BASE_URL}/chat/completions",
                headers=headers,
                json=payload,
                timeout=60,
            )
            response.raise_for_status()
            data = response.json()
            return data["choices"][0]["message"]["content"]
        except requests.exceptions.HTTPError as e:
            if response.status_code == 429:
                wait = 2 ** attempt
                time.sleep(wait)
                continue
            raise
        except Exception:
            if attempt == max_retries - 1:
                raise
            time.sleep(1)

    raise RuntimeError("LLM API call failed after retries")
