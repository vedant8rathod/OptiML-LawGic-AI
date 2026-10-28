from __future__ import annotations

from typing import Optional

from typing import Optional
from sqlalchemy.engine import Engine

from langchain_community.vectorstores.pgvector import PGVector

from .config import settings
from .db import ensure_pgvector as _ensure_pgvector
from .embeddings import get_embeddings


def ensure_table(engine: Optional[Engine] = None) -> None:
    """Ensure pgvector extension exists.

    PGVector will manage its own tables/collections when first used.
    """
    _ensure_pgvector()


def get_vectorstore(collection_name: Optional[str] = None) -> PGVector:
    """Initialize PGVector vector store from settings."""
    return PGVector(
        connection_string=settings.database_url,
        embedding_function=get_embeddings(),
        collection_name=collection_name or settings.pgvector_table,
    )
