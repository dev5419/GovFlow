"""
Unit tests for the Bidders module — service, repository, and router.

Acceptance criteria (PRD §8.1, F-01):
- Loads bidder data for the active tender.
- Every bidder in the response shows current document and compliance status.
- Tender context (tender_id) is required and validated on every call.
- Sort/filter logic works correctly on the aggregation-to-DTO mapping.
"""

import pytest
from datetime import datetime, timezone
from unittest.mock import AsyncMock, patch, MagicMock

from govflow_shared_types import BidderComplianceSummary
from src.modules.bidders.service import _model_to_dto, list_bidder_summaries
from src.modules.bidders.schemas import BidderSortField, BidderStatusFilter, SortOrder
from src.modules.bidders.repository import _FILTER_STATUS_MAP, _SORT_COLUMNS


# ---------------------------------------------------------------------------
# Fixtures: fake ORM rows
# ---------------------------------------------------------------------------

def _make_row(
    bidder_id: str = "b-001",
    tender_id: str = "t-001",
    bidder_name: str = "Acme Corp",
    compliance_score: float = 85.0,
    total_documents: int = 5,
    submitted_documents: int = 4,
    missing_documents: int = 1,
    verified_flags_count: int = 3,
    needs_review_flags_count: int = 1,
    non_compliance_flags_count: int = 0,
    confirmed_flags_count: int = 2,
    unresolved_flags_count: int = 1,
    processing_status: str = "completed",
    primary_risk_reasons: list | None = None,
    overall_status: str = "Needs Review",
) -> MagicMock:
    """Create a mock ORM row that looks like BidderComplianceSummaryModel."""
    row = MagicMock()
    row.bidder_id = bidder_id
    row.tender_id = tender_id
    row.bidder_name = bidder_name
    row.compliance_score = compliance_score
    row.total_documents = total_documents
    row.submitted_documents = submitted_documents
    row.missing_documents = missing_documents
    row.verified_flags_count = verified_flags_count
    row.needs_review_flags_count = needs_review_flags_count
    row.non_compliance_flags_count = non_compliance_flags_count
    row.confirmed_flags_count = confirmed_flags_count
    row.unresolved_flags_count = unresolved_flags_count
    row.processing_status = processing_status
    row.primary_risk_reasons = primary_risk_reasons if primary_risk_reasons is not None else ["Missing GST Certificate"]
    row.overall_status = overall_status
    row.updated_at = datetime(2026, 8, 30, 12, 0, 0, tzinfo=timezone.utc)
    return row


# ---------------------------------------------------------------------------
# Tests: DTO mapping (_model_to_dto)
# ---------------------------------------------------------------------------

class TestModelToDto:
    """Verify ORM row → shared-types BidderComplianceSummary mapping."""

    def test_basic_mapping(self):
        """Every bidder shows current document and compliance status."""
        row = _make_row()
        dto = _model_to_dto(row)

        assert isinstance(dto, BidderComplianceSummary)
        assert dto.bidder_id == "b-001"
        assert dto.tender_id == "t-001"
        assert dto.bidder_name == "Acme Corp"
        assert dto.compliance_score == 85.0
        assert dto.total_documents == 5
        assert dto.submitted_documents == 4
        assert dto.missing_documents == 1
        assert dto.verified_flags_count == 3
        assert dto.needs_review_flags_count == 1
        assert dto.non_compliance_flags_count == 0
        assert dto.confirmed_flags_count == 2
        assert dto.unresolved_flags_count == 1
        assert dto.processing_status == "completed"
        assert dto.primary_risk_reasons == ["Missing GST Certificate"]
        assert dto.overall_status == "Needs Review"

    def test_updated_at_iso_format(self):
        row = _make_row()
        dto = _model_to_dto(row)
        assert "2026-08-30" in dto.updated_at
        assert "T" in dto.updated_at

    def test_empty_risk_reasons(self):
        row = _make_row(primary_risk_reasons=[])
        dto = _model_to_dto(row)
        assert dto.primary_risk_reasons == []

    def test_none_risk_reasons_defaults_to_empty(self):
        row = _make_row()
        row.primary_risk_reasons = None
        dto = _model_to_dto(row)
        assert dto.primary_risk_reasons == []


# ---------------------------------------------------------------------------
# Tests: service layer
# ---------------------------------------------------------------------------

class TestListBidderSummaries:
    """Loads bidder data for the active tender."""

    @pytest.mark.asyncio
    async def test_returns_dto_list(self):
        """Loads bidder data for the active tender and returns DTOs."""
        mock_db = AsyncMock()
        rows = [_make_row(bidder_id="b-001"), _make_row(bidder_id="b-002", bidder_name="Beta Ltd")]

        with patch(
            "src.modules.bidders.service.repository.get_bidder_summaries",
            new_callable=AsyncMock,
            return_value=rows,
        ):
            result = await list_bidder_summaries(mock_db, "t-001")

        assert len(result) == 2
        assert all(isinstance(r, BidderComplianceSummary) for r in result)
        assert result[0].bidder_id == "b-001"
        assert result[1].bidder_id == "b-002"

    @pytest.mark.asyncio
    async def test_passes_filter_and_sort_to_repo(self):
        """Sort/filter params are forwarded to the repository layer."""
        mock_db = AsyncMock()

        with patch(
            "src.modules.bidders.service.repository.get_bidder_summaries",
            new_callable=AsyncMock,
            return_value=[],
        ) as mock_repo:
            await list_bidder_summaries(
                mock_db,
                "t-001",
                status_filter="compliant",
                sort_by="missing_documents",
                sort_order="desc",
            )

        mock_repo.assert_awaited_once_with(
            mock_db,
            "t-001",
            status_filter="compliant",
            sort_by="missing_documents",
            sort_order="desc",
        )

    @pytest.mark.asyncio
    async def test_empty_tender_returns_empty_list(self):
        """Tender context (tender_id) with no bidders returns empty list."""
        mock_db = AsyncMock()

        with patch(
            "src.modules.bidders.service.repository.get_bidder_summaries",
            new_callable=AsyncMock,
            return_value=[],
        ):
            result = await list_bidder_summaries(mock_db, "t-empty")

        assert result == []


# ---------------------------------------------------------------------------
# Tests: filter/sort mappings (repository constants)
# ---------------------------------------------------------------------------

class TestFilterStatusMap:
    """Verify filter status mapping completeness for PRD §8.1 dashboard filters."""

    def test_all_filter_values_mapped(self):
        for f in BidderStatusFilter:
            assert f.value in _FILTER_STATUS_MAP or f.value.replace("_", "-") in _FILTER_STATUS_MAP, (
                f"Filter '{f.value}' is not mapped in _FILTER_STATUS_MAP"
            )

    def test_compliant_maps_correctly(self):
        assert _FILTER_STATUS_MAP["compliant"] == "Compliant"

    def test_needs_review_maps_correctly(self):
        assert _FILTER_STATUS_MAP["needs_review"] == "Needs Review"

    def test_non_compliant_maps_correctly(self):
        assert _FILTER_STATUS_MAP["non_compliant"] == "Non-Compliant"

    def test_missing_maps_correctly(self):
        assert _FILTER_STATUS_MAP["missing"] == "Missing Documents"

    def test_processing_maps_correctly(self):
        assert _FILTER_STATUS_MAP["processing"] == "Processing"


class TestSortColumns:
    """Verify sort column mapping covers all allowed sort fields."""

    def test_all_sort_fields_mapped(self):
        for f in BidderSortField:
            assert f.value in _SORT_COLUMNS, f"Sort field '{f.value}' is not mapped in _SORT_COLUMNS"


# ---------------------------------------------------------------------------
# Tests: schemas (enum values sanity)
# ---------------------------------------------------------------------------

class TestSchemaEnums:
    """Validate enum values match PRD §8.1 expectations."""

    def test_sort_field_values(self):
        values = {f.value for f in BidderSortField}
        assert values == {"compliance_risk", "missing_documents", "processing_status"}

    def test_status_filter_values(self):
        values = {f.value for f in BidderStatusFilter}
        assert values == {"compliant", "needs_review", "non_compliant", "missing", "processing"}

    def test_sort_order_values(self):
        values = {f.value for f in SortOrder}
        assert values == {"asc", "desc"}
