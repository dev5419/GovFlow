from sqlalchemy import Column, String, Integer, Float, DateTime
from sqlalchemy.sql import func
from src.database import Base

class BidderComplianceSummaryModel(Base):
    __tablename__ = "bidder_compliance_summaries"

    id = Column(String, primary_key=True, index=True)
    tender_id = Column(String, nullable=False, index=True)
    bidder_id = Column(String, nullable=False, index=True)
    
    overall_score = Column(Float, nullable=False, default=100.0)
    total_documents = Column(Integer, nullable=False, default=0)
    missing_documents = Column(Integer, nullable=False, default=0)
    confirmed_flags = Column(Integer, nullable=False, default=0)
    unresolved_flags = Column(Integer, nullable=False, default=0)
    processing_status = Column(String, nullable=False, default="processing")
    primary_risk_reasons = Column(String, nullable=True)

    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
