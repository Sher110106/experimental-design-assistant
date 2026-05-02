"""Configuration and API keys.

Set these as environment variables:
    export GROQ_API_KEY="your-key-here"
    export FIRECRAWL_API_KEY="your-key-here"
"""
import os
from dotenv import load_dotenv

load_dotenv()

LLM_API_KEY = os.getenv("GROQ_API_KEY", "")
FIRECRAWL_API_KEY = os.getenv("FIRECRAWL_API_KEY", "")

LLM_BASE_URL = "https://api.groq.com/openai/v1"
FIRECRAWL_BASE_URL = "https://api.firecrawl.dev/v1"

DEFAULT_MODEL = "openai/gpt-oss-120b"
