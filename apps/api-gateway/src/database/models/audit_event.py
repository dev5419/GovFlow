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
