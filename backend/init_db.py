#!/usr/bin/env python3
"""
Initialize the database for the LawGic AI backend.
Creates all tables and sets up the demo environment.
"""

import os
import sys
from pathlib import Path

# Add the app directory to Python path
sys.path.insert(0, str(Path(__file__).parent / "app"))

from app.db.database import Base, engine, DATABASE_URL
from app.db.models import Document

def init_database():
    """Initialize the database tables."""
    print(f"Initializing database at: {DATABASE_URL}")
    
    try:
        # Create all tables
        Base.metadata.create_all(bind=engine)
        print("✅ Database tables created successfully!")
        print("📋 Tables created:")
        for table_name in Base.metadata.tables.keys():
            print(f"  - {table_name}")
        
    except Exception as e:
        print(f"❌ Error creating database: {e}")
        return False
    
    return True

if __name__ == "__main__":
    success = init_database()
    if success:
        print("\n🎉 Database initialization complete!")
        print("💡 You can now start the FastAPI server with: uvicorn app.main:app --reload")
    else:
        print("\n💥 Database initialization failed!")
        sys.exit(1)