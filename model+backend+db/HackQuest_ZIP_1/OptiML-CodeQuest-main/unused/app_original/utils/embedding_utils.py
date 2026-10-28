import os
import asyncio
import time
from typing import List

import google.generativeai as genai


def _clean_key(s: str | None) -> str | None:
    if not s:
        return s
    s = s.strip()
    if (s.startswith("\"") and s.endswith("\"")) or (s.startswith("'") and s.endswith("'")):
        return s[1:-1].strip()
    return s


# Read the API key from environment correctly
GOOGLE_API_KEY = _clean_key(os.getenv("GOOGLE_API_KEY"))
if GOOGLE_API_KEY:
    genai.configure(api_key=GOOGLE_API_KEY)


async def get_embedding(text: str) -> List[float]:
    """Return vector embedding using Gemini text-embedding-004.

    Uses small retry with exponential backoff. Falls back to zero-vector if key is missing or call fails.
    Wrapped in a thread to keep FastAPI handlers responsive.
    """

    def _embed_sync() -> List[float]:
        # Fallback when no API key is provided
        if not GOOGLE_API_KEY:
            return [0.0] * 768
        # Retry loop
        delay = 0.5
        for attempt in range(1, 4):
            try:
                res = genai.embed_content(model="text-embedding-004", content=text)
                emb = res.get("embedding") if isinstance(res, dict) else getattr(res, "embedding", None)
                if isinstance(emb, dict):
                    values = emb.get("values", [])
                    return values if isinstance(values, list) and values else [0.0] * 768
                return emb if isinstance(emb, list) and emb else [0.0] * 768
            except Exception:
                if attempt == 3:
                    break
                time.sleep(delay)
                delay *= 2
        # Best-effort fallback to deterministic size
        return [0.0] * 768

    return await asyncio.to_thread(_embed_sync)