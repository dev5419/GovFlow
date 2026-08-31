from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.session import get_db
from src.modules.auth.dependencies import get_current_procurement_officer, get_current_active_user
from src.database.models.user import UserModel
from src.modules.compliance.schemas import ComplianceFlagResponse, OfficerDecisionCreate
from src.modules.compliance.service import ComplianceService

router = APIRouter(prefix="", tags=["compliance"])

@router.get("/tenders/{tender_id}/bidders/{bidder_id}/flags", response_model=List[ComplianceFlagResponse])
async def get_compliance_flags(
    tender_id: str, 
    bidder_id: str, 
    db: AsyncSession = Depends(get_db),
    # Any active user can read (e.g., Compliance Auditor, Tender Committee Member)
    user: UserModel = Depends(get_current_active_user)
):
    """
    Retrieve all ComplianceFlags for a bidder. Read-only.
    """
    return await ComplianceService.get_flags(db, tender_id, bidder_id)


@router.post("/flags/{flag_id}/decisions", status_code=201)
async def record_officer_decision(
    flag_id: str, 
    decision: OfficerDecisionCreate,
    db: AsyncSession = Depends(get_db),
    # Only Procurement Officer (or Admin) can record a decision
    user: UserModel = Depends(get_current_procurement_officer)
):
    """
    Record an OfficerDecision against a ComplianceFlag. 
    Appends an AuditEvent in the same transaction.
    """
    return await ComplianceService.record_decision(
        db=db,
        flag_id=flag_id,
        user=user,
        decision_state=decision.decisionState,
        notes=decision.notes
    )
