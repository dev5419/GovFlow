from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql import func
from src.database import Base

class ComplianceFlagModel(Base):
    __tablename__ = "compliance_flags"

    id = Column(String, primary_key=True, index=True)
    tender_id = Column(String, nullable=False, index=True)
    bidder_id = Column(String, nullable=False, index=True)
    rule_id = Column(String, nullable=True) 
    
    status = Column(String, nullable=False) 
    severity = Column(String, nullable=False)
    
    title = Column(String, nullable=False)
    reason = Column(String, nullable=False)
    ai_recommendation = Column(String, nullable=False)
    
    anchors = Column(JSONB, default=list, nullable=False)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
