from __future__ import annotations

from typing import Optional

from langchain_google_genai import GoogleGenerativeAIEmbeddings

from .config import settings

_embeddings: Optional[GoogleGenerativeAIEmbeddings] = None


def get_embeddings(api_key: Optional[str] = None) -> GoogleGenerativeAIEmbeddings:
    """Singleton for GoogleGenerativeAIEmbeddings.

    The embedding model used by Gemini is set to `text-embedding-004` by default.
    """
    global _embeddings
    if _embeddings is None:
        _embeddings = GoogleGenerativeAIEmbeddings(
            model="text-embedding-004",
            google_api_key=api_key or settings.google_api_key,
        )
    return _embeddings
