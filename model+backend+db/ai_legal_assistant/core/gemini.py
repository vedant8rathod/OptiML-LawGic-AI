from __future__ import annotations

from typing import Optional

from .config import settings

_configured: Optional[bool] = None


def ensure_gemini_configured() -> None:
    """Configure google-generativeai to use API v1 with the provided API key.

    Safe to call multiple times; configuration is applied once per process.
    """
    global _configured
    if _configured:
        return
    try:
        import google.generativeai as genai  # type: ignore
        genai.configure(api_key=settings.google_api_key)
        _configured = True
    except Exception:
        # If the SDK isn't installed, caller may be using simulated path.
        _configured = False