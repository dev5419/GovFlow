from sqlalchemy import Column, String, DateTime, Enum, ForeignKey
from sqlalchemy.sql import func
from src.database.session import Base
import enum

class ReportStatus(str, enum.Enum):
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"

class ReportModel(Base):
    __tablename__ = "reports"

    id = Column(String, primary_key=True, index=True)
    tender_id = Column(String, nullable=False, index=True)
    bidder_id = Column(String, nullable=False, index=True)
    
    status = Column(Enum(ReportStatus), default=ReportStatus.PENDING, nullable=False)
    object_key = Column(String, nullable=True) # Set when COMPLETED
    
    requested_by = Column(String, nullable=False)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
