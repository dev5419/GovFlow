from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.session import get_db
from src.modules.auth.dependencies import get_current_active_user
from src.database.models.user import UserModel
from src.modules.audit.schemas import AuditEventResponse
from src.modules.audit.service import AuditService

router = APIRouter(prefix="/audit", tags=["audit"])

@router.get("/flags/{flag_id}", response_model=List[AuditEventResponse])
async def get_flag_audit_history(
    flag_id: str, 
    db: AsyncSession = Depends(get_db),
    user: UserModel = Depends(get_current_active_user)
):
    """
    Retrieve the complete, append-only decision history for a flag.
    """
    return await AuditService.get_by_flag(db, flag_id)

@router.get("/bidders/{bidder_id}", response_model=List[AuditEventResponse])
async def get_bidder_audit_history(
    bidder_id: str, 
    db: AsyncSession = Depends(get_db),
    user: UserModel = Depends(get_current_active_user)
):
    """
    Retrieve the complete, append-only decision history for a bidder's package.
    """
    return await AuditService.get_by_bidder(db, bidder_id)
