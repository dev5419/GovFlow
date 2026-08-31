"""
GovFlow SQLAlchemy ORM Models for Document, DocumentPage, and ProcessingJob.
Matches entities defined in GovFlow_PRD.md §10 and packages/shared-types.
"""

import uuid
from datetime import datetime, timezone
from sqlalchemy import (
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import relationship

from src.database import Base


def _utcnow():
    return datetime.now(timezone.utc)


def _new_id():
    return str(uuid.uuid4())


class DocumentModel(Base):
    """SQLAlchemy ORM model for Document entity per PRD §10."""
    __tablename__ = "documents"

    id = Column(String, primary_key=True, default=_new_id)
    tender_id = Column(String, nullable=False, index=True)
    bidder_id = Column(String, nullable=False, index=True)
    required_document_id = Column(String, nullable=True)
    document_type = Column(String, nullable=True)
    file_name = Column(String, nullable=False)
    file_size = Column(Integer, nullable=False, default=0)
    file_type = Column(String, nullable=False)
    storage_path = Column(String, nullable=False)
    page_count = Column(Integer, nullable=False, default=0)
    status = Column(String, nullable=False, default="uploaded")
    error_message = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), nullable=False, default=_utcnow)
    updated_at = Column(DateTime(timezone=True), nullable=False, default=_utcnow, onupdate=_utcnow)

    pages = relationship(
        "DocumentPageModel",
        back_populates="document",
        cascade="all, delete-orphan",
        order_by="DocumentPageModel.page_number",
    )


class DocumentPageModel(Base):
    """SQLAlchemy ORM model for DocumentPage entity per PRD §10."""
    __tablename__ = "document_pages"

    id = Column(String, primary_key=True, default=_new_id)
    document_id = Column(
        String,
        ForeignKey("documents.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    page_number = Column(Integer, nullable=False)
    page_width = Column(Integer, nullable=False)
    page_height = Column(Integer, nullable=False)
    image_storage_path = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), nullable=False, default=_utcnow)

    document = relationship("DocumentModel", back_populates="pages")


class ProcessingJobModel(Base):
    """SQLAlchemy ORM model for ProcessingJob tracking per PRD §10."""
    __tablename__ = "processing_jobs"

    id = Column(String, primary_key=True, default=_new_id)
    tender_id = Column(String, nullable=False, index=True)
    bidder_id = Column(String, nullable=True, index=True)
    document_id = Column(String, nullable=True, index=True)
    job_type = Column(String, nullable=False, default="ingestion")
    status = Column(String, nullable=False, default="queued")
    progress = Column(Float, nullable=False, default=0.0)
    current_step = Column(String, nullable=True)
    error_message = Column(Text, nullable=True)
    retry_count = Column(Integer, nullable=False, default=0)
    created_at = Column(DateTime(timezone=True), nullable=False, default=_utcnow)
    updated_at = Column(DateTime(timezone=True), nullable=False, default=_utcnow, onupdate=_utcnow)
    completed_at = Column(DateTime(timezone=True), nullable=True)
