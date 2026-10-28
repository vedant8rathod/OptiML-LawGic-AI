from sqlalchemy import Column, Integer, String, Text, DateTime, func, JSON
from sqlalchemy.orm import relationship
from .database import Base

class Document(Base):
    __tablename__ = "documents"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=True)
    filename = Column(String, nullable=False)
    content = Column(Text)
    doc_metadata = Column(JSON, default={})  # Renamed to avoid conflict
    embedding = Column(Text)  # Store as JSON string for SQLite compatibility
    created_at = Column(DateTime(timezone=True), server_default=func.now())
