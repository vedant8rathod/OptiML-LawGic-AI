import os
import asyncio
from typing import List

import google.generativeai as genai

# Configure Gemini API (v1)
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)


async def get_embedding(text: str) -> List[float]:
    """Return vector embedding using Gemini text-embedding-004.

    This wraps the sync SDK call in a thread so FastAPI handlers remain responsive.
    """

    def _embed_sync() -> List[float]:
        # Local fallback when no API key is provided
        if not GOOGLE_API_KEY:
            return [0.0] * 768
        try:
            res = genai.embed_content(model="text-embedding-004", content=text)
            # google-generativeai returns { 'embedding': { 'values': [...] } } or { 'embedding': [...] } depending on version
            emb = res.get("embedding") if isinstance(res, dict) else getattr(res, "embedding", None)
            if isinstance(emb, dict):
                return emb.get("values", [])
            return emb or []
        except Exception:
            # Best-effort fallback to deterministic size
            return [0.0] * 768

    return await asyncio.to_thread(_embed_sync)