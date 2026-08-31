from sqlalchemy import Column, String, DateTime, Enum, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql import func
from src.database import Base
from govflow_shared_types import ComplianceFlagStatus

class ComplianceFlagModel(Base):
    __tablename__ = "compliance_flags"

    id = Column(String, primary_key=True, index=True)
    tender_id = Column(String, nullable=False, index=True)
    bidder_id = Column(String, nullable=False, index=True)
    rule_id = Column(String, nullable=True) # E.g., system-rule-gstin_match or actual TenderRule ID
    
    # Store enum values as strings in DB
    status = Column(String, nullable=False) 
    severity = Column(String, nullable=False)
    
    title = Column(String, nullable=False)
    reason = Column(String, nullable=False)
    ai_recommendation = Column(String, nullable=False)
    
    # We store anchors here to avoid joining another table if we just need the JSON
    anchors = Column(JSONB, default=list, nullable=False)
    
    # To support immutability, we don't have update_at, only created_at.
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
