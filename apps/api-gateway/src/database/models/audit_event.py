import uuid
from sqlalchemy import Column, String, DateTime
from sqlalchemy.sql import func
from src.database import Base

class AuditEventModel(Base):
    """
    Immutable, append-only record for all compliance decisions per PRD 9.2.
    """
    __tablename__ = "audit_events"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    
    tender_id = Column(String, nullable=False, index=True)
    bidder_id = Column(String, nullable=False, index=True)
    document_id = Column(String, nullable=True, index=True)
    compliance_flag_id = Column(String, nullable=True, index=True)
    
    officer_user_id = Column(String, nullable=False)
    officer_role = Column(String, nullable=False)
    
    original_ai_recommendation = Column(String, nullable=True)
    officer_decision = Column(String, nullable=False)
    officer_notes = Column(String, nullable=True)
    
    previous_decision_state = Column(String, nullable=True)
    new_decision_state = Column(String, nullable=False)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)


class AccessLogModel(Base):
    """
    Immutable read-receipt log for all document/evidence accesses per PRD 21.2/21.3.
    """
    __tablename__ = "access_logs"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    
    user_id = Column(String, nullable=False, index=True)
    resource_type = Column(String, nullable=False) # e.g., "DOCUMENT_IMAGE", "EVIDENCE_OVERLAY", "LINKED_EVIDENCE"
    resource_id = Column(String, nullable=False, index=True) # e.g., document_id, anchor_id
    
    ip_address = Column(String, nullable=True)
    user_agent = Column(String, nullable=True)
    
    accessed_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
