import uuid
from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from src.database import Base

class OfficerDecisionModel(Base):
    """
    Records an Officer's decision on a specific ComplianceFlag.
    """
    __tablename__ = "officer_decisions"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    
    compliance_flag_id = Column(String, nullable=False, index=True) # We won't strictly enforce ForeignKey if flag is in another db, but they share the same DB.
    officer_user_id = Column(String, ForeignKey("users.id"), nullable=False, index=True)
    
    # Confirmed, Rejected, Overridden, Escalated
    decision_state = Column(String, nullable=False)
    
    notes = Column(String, nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
