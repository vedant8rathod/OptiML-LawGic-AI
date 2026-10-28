from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Optional

try:
    from dotenv import load_dotenv  # type: ignore
    load_dotenv()
except Exception:
    # If python-dotenv is not installed or .env load fails, proceed with OS env only
    pass


@dataclass
class Settings:
    """Environment-driven configuration for the AI Legal Assistant."""

    # Google Gemini / Generative AI
    google_api_key: Optional[str] = os.getenv("GOOGLE_API_KEY")

    # PostgreSQL with pgvector
    database_url: Optional[str] = os.getenv("DATABASE_URL")  # e.g. postgresql+psycopg2://user:pass@host:5432/db
    pgvector_dim: int = int(os.getenv("PGVECTOR_DIM", "768"))
    pgvector_table: str = os.getenv("PGVECTOR_TABLE", "legal_embeddings")

    # spaCy model name
    spacy_model: str = os.getenv("SPACY_MODEL", "en_core_web_sm")

    # Indexing
    documents_dir: str = os.getenv("DOCUMENTS_DIR", "./documents")


settings = Settings()
