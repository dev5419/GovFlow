"""
GovFlow AI Workers Database Session Management
Provides SQLAlchemy engine and session factory for PostgreSQL 15.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from src.shared.config import settings

engine = create_engine(settings.database_url, echo=False, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db_session():
    """Context-managed database session for worker tasks."""
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
