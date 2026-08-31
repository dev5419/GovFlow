"""
Bidder module schemas — re-exports shared-types and defines query param enums.
No local redefinition of Bidder or BidderComplianceSummary.
"""

from enum import Enum

from govflow_shared_types import (
    Bidder,
    BidderComplianceSummary,
)


class BidderSortField(str, Enum):
    """Allowed sort keys for the bidder dashboard list."""
    compliance_risk = "compliance_risk"
    missing_documents = "missing_documents"
    processing_status = "processing_status"


class BidderStatusFilter(str, Enum):
    """Allowed filter values matching PRD §8.1 dashboard filters."""
    compliant = "compliant"
    needs_review = "needs_review"
    non_compliant = "non_compliant"
    missing = "missing"
    processing = "processing"


class SortOrder(str, Enum):
    asc = "asc"
    desc = "desc"
