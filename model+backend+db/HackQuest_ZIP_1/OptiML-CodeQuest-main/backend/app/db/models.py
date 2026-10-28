from __future__ import annotations

import os

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.types import JSON

from .database import Base

try:
    from pgvector.sqlalchemy import Vector  # type: ignore
except Exception as exc:
    raise RuntimeError(
        "pgvector is required but not installed. Ensure the python package and Postgres extension are available."
    ) from exc

USE_PGVECTOR = os.getenv("USE_PGVECTOR", "1").strip() != "0"


class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=True)
    filename = Column(String, nullable=False)
    content = Column(Text)
    meta = Column(JSONB, default={})
    # Keep the raw embedding payload alongside the pgvector entry for troubleshooting.
    embedding = Column(JSON)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    embeddings = relationship("Embedding", back_populates="document", cascade="all, delete-orphan")
    analyses = relationship("ContractAnalysisResult", back_populates="document", cascade="all, delete-orphan")


class Embedding(Base):
    __tablename__ = "embeddings"

    id = Column(Integer, primary_key=True)
    document_id = Column(Integer, ForeignKey("documents.id", ondelete="CASCADE"), nullable=False, index=True)
    vector = Column(Vector(768))  # type: ignore[arg-type]
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    document = relationship("Document", back_populates="embeddings")


class ContractAnalysisResult(Base):
    __tablename__ = "contract_analysis_results"

    id = Column(Integer, primary_key=True)
    document_id = Column(Integer, ForeignKey("documents.id", ondelete="CASCADE"), nullable=False, index=True)
    result = Column(JSONB, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    document = relationship("Document", back_populates="analyses")