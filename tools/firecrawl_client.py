"""Firecrawl API client for web search."""
import time
import requests
from config import FIRECRAWL_API_KEY, FIRECRAWL_BASE_URL


def search_datasets(query: str, max_retries: int = 2) -> list[dict]:
    """Search for datasets using Firecrawl."""
    headers = {
        "Authorization": f"Bearer {FIRECRAWL_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "query": query,
        "limit": 5,
    }

    for attempt in range(max_retries):
        try:
            response = requests.post(
                f"{FIRECRAWL_BASE_URL}/search",
                headers=headers,
                json=payload,
                timeout=30,
            )
            response.raise_for_status()
            data = response.json()
            results = data.get("data", [])
            datasets = []
            for r in results:
                datasets.append({
                    "name": r.get("title", "Unknown"),
                    "source": r.get("metadata", {}).get("source", "Web"),
                    "description": r.get("description", "")[:200],
                    "url": r.get("url", ""),
                })
            return datasets
        except Exception:
            if attempt == max_retries - 1:
                return []
            time.sleep(2)

    return []
