"""
GovFlow SQLAlchemy ORM Model for ExtractedField.
Matches entities defined in GovFlow_PRD.md §10 and packages/shared-types.
"""

import uuid
from datetime import datetime, timezone
from sqlalchemy import (
    Column,
    DateTime,
    Float,
    Integer,
    String,
    Text,
)
from sqlalchemy.dialects.postgresql import JSONB
from src.database import Base

def _utcnow():
    return datetime.now(timezone.utc)

def _new_id():
    return str(uuid.uuid4())

class ExtractedFieldModel(Base):
    """SQLAlchemy ORM model for ExtractedField entity per PRD §10 and §8.3."""
    __tablename__ = "extracted_fields"

    id = Column(String, primary_key=True, default=_new_id)
    document_id = Column(String, nullable=False, index=True)
    page_number = Column(Integer, nullable=False)
    field_name = Column(String, nullable=False, index=True)
    raw_text = Column(Text, nullable=False)
    normalized_value = Column(JSONB, nullable=True)
    confidence = Column(Float, nullable=False)
    bounding_box = Column(JSONB, nullable=False)
    extraction_method = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False, default=_utcnow)
