import uuid
from sqlalchemy import Column, String, Boolean, DateTime
from sqlalchemy.sql import func
from src.database import Base

class UserModel(Base):
    """
    User model for FastAPI-Users and RBAC.
    """
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    is_superuser = Column(Boolean, default=False, nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)
    
    # Roles: Procurement Officer, Compliance Auditor, Tender Committee Member, System Administrator
    role = Column(String, nullable=False, default="Procurement Officer")
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
