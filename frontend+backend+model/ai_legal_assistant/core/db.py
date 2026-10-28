from __future__ import annotations

from typing import Optional

from sqlalchemy import text, create_engine
from sqlalchemy.engine import Engine

from .config import settings

_engine: Optional[Engine] = None


def get_engine(url: Optional[str] = None) -> Engine:
    global _engine
    if _engine is None:
        _engine = create_engine(url or settings.database_url, pool_pre_ping=True)
    return _engine


def ensure_pgvector(engine: Optional[Engine] = None) -> None:
    """Ensure pgvector extension exists."""
    engine = engine or get_engine()
    with engine.begin() as conn:
        conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
