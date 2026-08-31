"""
Bidder module service — maps ORM rows to shared-types DTOs.
Read-only; emits no events (PRD §8.1 is a query surface).
"""

from typing import List

from sqlalchemy.ext.asyncio import AsyncSession

from govflow_shared_types import BidderComplianceSummary
from src.database.models.bidder import BidderComplianceSummaryModel
from src.modules.bidders import repository


def _model_to_dto(row: BidderComplianceSummaryModel) -> BidderComplianceSummary:
    """Map a SQLAlchemy ORM row to the shared-types Pydantic model."""
    return BidderComplianceSummary(
        bidder_id=row.bidder_id,
        tender_id=row.tender_id,
        bidder_name=row.bidder_name,
        compliance_score=row.compliance_score,
        total_documents=row.total_documents,
        submitted_documents=row.submitted_documents,
        missing_documents=row.missing_documents,
        verified_flags_count=row.verified_flags_count,
        needs_review_flags_count=row.needs_review_flags_count,
        non_compliance_flags_count=row.non_compliance_flags_count,
        confirmed_flags_count=row.confirmed_flags_count,
        unresolved_flags_count=row.unresolved_flags_count,
        processing_status=row.processing_status,
        primary_risk_reasons=list(row.primary_risk_reasons or []),
        overall_status=row.overall_status,
        updated_at=row.updated_at.isoformat() if row.updated_at else "",
    )


async def list_bidder_summaries(
    db: AsyncSession,
    tender_id: str,
    *,
    status_filter: str | None = None,
    sort_by: str | None = None,
    sort_order: str = "asc",
) -> List[BidderComplianceSummary]:
    """
    Return pre-aggregated bidder compliance summaries for a tender.
    Dashboard views load from pre-aggregated data (PRD §22).
    """
    rows = await repository.get_bidder_summaries(
        db,
        tender_id,
        status_filter=status_filter,
        sort_by=sort_by,
        sort_order=sort_order,
    )
    return [_model_to_dto(r) for r in rows]
