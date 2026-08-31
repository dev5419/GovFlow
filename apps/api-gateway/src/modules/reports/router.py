from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.session import get_db
from src.modules.auth.dependencies import get_current_active_user, RoleChecker
from src.database.models.user import UserModel
from src.modules.reports.schemas import ReportResponse
from src.modules.reports.service import ReportService

router = APIRouter(prefix="/tenders/{tender_id}/bidders/{bidder_id}/reports", tags=["reports"])

# Read roles: Officer, Auditor, Committee
allow_read_roles = RoleChecker(["Procurement Officer", "Compliance Auditor", "Tender Committee Member"])
# Write roles: Officer
allow_write_roles = RoleChecker(["Procurement Officer"])

@router.post("", response_model=ReportResponse)
async def request_report(
    tender_id: str,
    bidder_id: str,
    db: AsyncSession = Depends(get_db),
    user: UserModel = Depends(allow_write_roles)
):
    """
    Request a new compliance report generation.
    Only Procurement Officers can trigger this (write action).
    Creates a new independent tracking record every time.
    """
    return await ReportService.request_report(db, tender_id, bidder_id, user.id)

@router.get("", response_model=List[ReportResponse])
async def list_reports(
    tender_id: str,
    bidder_id: str,
    db: AsyncSession = Depends(get_db),
    user: UserModel = Depends(allow_read_roles)
):
    """
    List all generated and pending reports for a bidder.
    Accessible to Officers, Auditors, and Committee Members.
    """
    return await ReportService.get_reports(db, tender_id, bidder_id)

@router.get("/{report_id}", response_model=ReportResponse)
async def get_report(
    tender_id: str,
    bidder_id: str,
    report_id: str,
    db: AsyncSession = Depends(get_db),
    user: UserModel = Depends(allow_read_roles)
):
    """
    Poll for a specific report's status and fetch download URL.
    """
    report = await ReportService.get_report_by_id(db, report_id)
    if not report or report["tender_id"] != tender_id or report["bidder_id"] != bidder_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Report not found")
    return report
