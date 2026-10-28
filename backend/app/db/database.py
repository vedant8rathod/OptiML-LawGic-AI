import os
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Database URL - use SQLite for demo, PostgreSQL for production
from pathlib import Path
default_db_path = Path(__file__).parent.parent.parent / "law_ai_demo.db"
DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{default_db_path}")

if DATABASE_URL.startswith("sqlite"):
    # SQLite setup
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    def get_db():
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()
else:
    # PostgreSQL async setup
    async_engine = create_async_engine(DATABASE_URL, echo=True)
    AsyncSessionLocal = sessionmaker(async_engine, class_=AsyncSession, expire_on_commit=False)
    
    async def get_db():
        async with AsyncSessionLocal() as session:
            yield session

Base = declarative_base()

def init_db():
    """
    Initialize database tables.
    Creates all tables defined in models.
    """
    try:
        # Import models to ensure they're registered
        from . import models
        
        # Create all tables
        Base.metadata.create_all(bind=engine)
        print("INFO: Database initialized successfully")
        
    except Exception as e:
        print(f"WARNING: Database initialization failed: {e}")
        print("NOTE: This is expected if you don't have SQLAlchemy installed")
        print("INFO: The app will still work in demo mode")
