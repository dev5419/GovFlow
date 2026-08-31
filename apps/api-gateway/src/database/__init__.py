"""
GovFlow Database Session Configuration
Provides async SQLAlchemy engine and session factory for PostgreSQL 15.
"""

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from src.config.settings import settings

# Convert sync URL to async: postgresql:// → postgresql+asyncpg://
_db_url = settings.database_url.replace("postgresql://", "postgresql+asyncpg://", 1)

engine = create_async_engine(_db_url, echo=settings.debug, future=True)

async_session_factory = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


class Base(DeclarativeBase):
    """Shared declarative base for all SQLAlchemy ORM models."""
    pass


async def get_db() -> AsyncSession:
    """FastAPI dependency that yields a per-request database session."""
    async with async_session_factory() as session:
        try:
            yield session
        finally:
            await session.close()
