from __future__ import annotations

import os
from typing import AsyncGenerator

from sqlalchemy import text
import asyncio
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import declarative_base

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://lawgic_user:lawgicpass@localhost:5432/lawgic")

if not DATABASE_URL.startswith("postgresql+asyncpg"):
    raise RuntimeError("DATABASE_URL must be a PostgreSQL async URL, e.g., postgresql+asyncpg://user:pass@host/db")

engine = create_async_engine(DATABASE_URL, future=True, echo=False)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
Base = declarative_base()


async def init_db() -> None:
    # Robust retry to handle container startup races or delayed extensions
    for attempt in range(1, 11):
        try:
            async with engine.begin() as conn:
                # Ensure pgvector is available; safe to run multiple times
                await conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
                from . import models  # register models
                await conn.run_sync(Base.metadata.create_all)
            return
        except Exception:
            if attempt == 10:
                raise
            await asyncio.sleep(min(0.5 * attempt, 5.0))


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session