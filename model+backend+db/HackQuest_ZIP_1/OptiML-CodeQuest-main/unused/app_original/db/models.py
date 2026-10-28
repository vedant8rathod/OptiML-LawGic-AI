from sqlalchemy import Column, Integer, String, Text, DateTime, func, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.types import JSON
from sqlalchemy.orm import relationship
from .database import Base
import os

try:
    from pgvector.sqlalchemy import Vector  # type: ignore
except Exception as e:
    raise RuntimeError("pgvector is required but not installed. Ensure 'pgvector' Python package and 'vector' extension in Postgres.") from e
USE_PGVECTOR = os.getenv("USE_PGVECTOR", "1").strip() != "0"

class Document(Base):
    __tablename__ = "documents"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=True)
    filename = Column(String, nullable=False)
    content = Column(Text)
    # Use JSONB on Postgres
    meta = Column(JSONB, default={})
    # Store raw embedding alongside for convenience/troubleshooting
    embedding = Column(JSON)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    embeddings = relationship("Embedding", back_populates="document", cascade="all, delete-orphan")
    analyses = relationship("ContractAnalysisResult", back_populates="document", cascade="all, delete-orphan")


class Embedding(Base):
    __tablename__ = "embeddings"
    id = Column(Integer, primary_key=True)
    document_id = Column(Integer, ForeignKey("documents.id", ondelete="CASCADE"), nullable=False, index=True)
    # Require pgvector for embeddings in Postgres
    vector = Column(Vector(768))  # type: ignore
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    document = relationship("Document", back_populates="embeddings")


class ContractAnalysisResult(Base):
    __tablename__ = "contract_analysis_results"
    id = Column(Integer, primary_key=True)
    document_id = Column(Integer, ForeignKey("documents.id", ondelete="CASCADE"), nullable=False, index=True)
    # Store the list of clause analyses as JSONB
    result = Column(JSONB, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    document = relationship("Document", back_populates="analyses")