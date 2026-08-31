"""
Bidder module router — read-only GET endpoints for the Tender Dashboard (F-01).
"""

from typing import List, Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from govflow_shared_types import BidderComplianceSummary
from src.database import get_db
from src.modules.bidders.schemas import BidderSortField, BidderStatusFilter, SortOrder
from src.modules.bidders.service import list_bidder_summaries

router = APIRouter(prefix="/tenders/{tender_id}/bidders", tags=["bidders"])


@router.get(
    "/summaries",
    response_model=List[BidderComplianceSummary],
    summary="Retrieve aggregated bidder list for the Tender Dashboard (F-01)",
    description=(
        "Returns pre-aggregated compliance summaries for all bidders in a tender. "
        "Supports sort by compliance_risk, missing_documents, or processing_status, "
        "and filter by compliant, needs_review, non_compliant, missing, or processing."
    ),
)
async def get_bidder_summaries(
    tender_id: str,
    status: Optional[BidderStatusFilter] = Query(
        default=None,
        description="Filter by dashboard status: compliant, needs_review, non_compliant, missing, processing",
    ),
    sort_by: Optional[BidderSortField] = Query(
        default=None,
        description="Sort column: compliance_risk, missing_documents, processing_status",
    ),
    sort_order: SortOrder = Query(
        default=SortOrder.asc,
        description="Sort direction: asc or desc",
    ),
    db: AsyncSession = Depends(get_db),
) -> List[BidderComplianceSummary]:
    return await list_bidder_summaries(
        db,
        tender_id,
        status_filter=status.value if status else None,
        sort_by=sort_by.value if sort_by else None,
        sort_order=sort_order.value,
    )
