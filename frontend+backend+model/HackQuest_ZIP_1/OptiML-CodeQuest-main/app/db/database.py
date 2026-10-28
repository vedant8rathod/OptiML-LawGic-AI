from __future__ import annotations

import os
from typing import AsyncGenerator

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import declarative_base

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://lawgic_user:lawgicpass@localhost:5432/lawgic")
IS_SQLITE = DATABASE_URL.startswith("sqlite")

engine = create_async_engine(DATABASE_URL, future=True, echo=False)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
Base = declarative_base()


async def init_db() -> None:
    async with engine.begin() as conn:
        if not IS_SQLITE:
            await conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
        from . import models  # register models
        await conn.run_sync(Base.metadata.create_all)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session