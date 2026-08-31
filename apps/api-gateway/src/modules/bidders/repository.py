"""
Bidder module repository — read-only queries against pre-aggregated tables.
"""

from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from src.database.models.bidder import BidderComplianceSummaryModel, BidderModel


# Maps external sort keys to column references
_SORT_COLUMNS = {
    "compliance_risk": BidderComplianceSummaryModel.compliance_score,       # lower = riskier → asc
    "missing_documents": BidderComplianceSummaryModel.missing_documents,    # higher = worse → desc
    "processing_status": BidderComplianceSummaryModel.processing_status,    # alphabetical
}

# Maps external filter keys to overall_status column values
_FILTER_STATUS_MAP = {
    "compliant": "Compliant",
    "needs_review": "Needs Review",         # ponytail: PRD §8.1 calls it "needs-review" in the URL
    "needs-review": "Needs Review",
    "non_compliant": "Non-Compliant",
    "non-compliant": "Non-Compliant",
    "missing": "Missing Documents",
    "processing": "Processing",
}


async def get_bidder_summaries(
    db: AsyncSession,
    tender_id: str,
    *,
    status_filter: Optional[str] = None,
    sort_by: Optional[str] = None,
    sort_order: str = "asc",
) -> List[BidderComplianceSummaryModel]:
    """
    Fetch pre-aggregated bidder compliance summaries for a tender.
    Filtering and sorting happen in SQL to keep the endpoint fast per PRD §22.
    """
    stmt = (
        select(BidderComplianceSummaryModel)
        .where(BidderComplianceSummaryModel.tender_id == tender_id)
    )

    # Apply status filter
    if status_filter:
        mapped = _FILTER_STATUS_MAP.get(status_filter.lower())
        if mapped:
            stmt = stmt.where(BidderComplianceSummaryModel.overall_status == mapped)

    # Apply sort
    col = _SORT_COLUMNS.get(sort_by)
    if col is not None:
        if sort_by == "compliance_risk":
            # Lower score = higher risk → ascending gives riskiest first
            stmt = stmt.order_by(col.asc() if sort_order == "asc" else col.desc())
        elif sort_by == "missing_documents":
            # More missing = worse → descending gives worst first
            stmt = stmt.order_by(col.desc() if sort_order == "asc" else col.asc())
        else:
            stmt = stmt.order_by(col.asc() if sort_order == "asc" else col.desc())
    else:
        # Default: riskiest first (lowest compliance score)
        stmt = stmt.order_by(BidderComplianceSummaryModel.compliance_score.asc())

    result = await db.execute(stmt)
    return list(result.scalars().all())
