from sqlalchemy import Column, Integer, String, Text, DateTime, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.types import JSON
from .database import Base, IS_SQLITE

class Document(Base):
    __tablename__ = "documents"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=True)
    filename = Column(String, nullable=False)
    content = Column(Text)
    # Use JSONB on Postgres and JSON on SQLite
    meta = Column(JSONB if not IS_SQLITE else JSON, default={})
    # Store embedding as JSON array universally to avoid pgvector requirement during local tests
    embedding = Column(JSON)
    created_at = Column(DateTime(timezone=True), server_default=func.now())