"""
GovFlow SQLAlchemy ORM Models — Bidder & BidderComplianceSummary
Tables match shared-types entities from packages/shared-types.
"""

import uuid
from datetime import datetime, timezone

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.dialects.postgresql import ARRAY, JSONB, UUID
from sqlalchemy.orm import relationship

from src.database import Base


def _utcnow():
    return datetime.now(timezone.utc)


def _new_id():
    return str(uuid.uuid4())


class BidderModel(Base):
    """SQLAlchemy ORM model for Bidder entity per PRD §10."""

    __tablename__ = "bidders"

    id = Column(String, primary_key=True, default=_new_id)
    tender_id = Column(String, nullable=False, index=True)
    name = Column(String, nullable=False)
    registration_number = Column(String, nullable=True)
    gstin = Column(String, nullable=True)
    pan = Column(String, nullable=True)
    udyam_number = Column(String, nullable=True)
    status = Column(String, nullable=False, default="submitted")
    created_at = Column(DateTime(timezone=True), nullable=False, default=_utcnow)
    updated_at = Column(DateTime(timezone=True), nullable=False, default=_utcnow, onupdate=_utcnow)

    compliance_summary = relationship(
        "BidderComplianceSummaryModel",
        back_populates="bidder",
        uselist=False,
        lazy="joined",
    )


class BidderComplianceSummaryModel(Base):
    """
    SQLAlchemy ORM model for BidderComplianceSummary per PRD §8.1 and §10.
    Pre-aggregated read model written by the Compliance Engine (Module 4).
    This endpoint only reads; it never writes to this table.
    """

    __tablename__ = "bidder_compliance_summaries"

    bidder_id = Column(
        String,
        ForeignKey("bidders.id", ondelete="CASCADE"),
        primary_key=True,
    )
    tender_id = Column(String, nullable=False, index=True)
    bidder_name = Column(String, nullable=False)
    compliance_score = Column(Float, nullable=False, default=0.0)
    total_documents = Column(Integer, nullable=False, default=0)
    submitted_documents = Column(Integer, nullable=False, default=0)
    missing_documents = Column(Integer, nullable=False, default=0)
    verified_flags_count = Column(Integer, nullable=False, default=0)
    needs_review_flags_count = Column(Integer, nullable=False, default=0)
    non_compliance_flags_count = Column(Integer, nullable=False, default=0)
    confirmed_flags_count = Column(Integer, nullable=False, default=0)
    unresolved_flags_count = Column(Integer, nullable=False, default=0)
    processing_status = Column(String, nullable=False, default="pending")
    primary_risk_reasons = Column(ARRAY(String), nullable=False, default=list)
    overall_status = Column(String, nullable=False, default="Processing")
    updated_at = Column(DateTime(timezone=True), nullable=False, default=_utcnow, onupdate=_utcnow)

    bidder = relationship("BidderModel", back_populates="compliance_summary")
