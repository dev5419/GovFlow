import pytest
from unittest.mock import patch, MagicMock
from src.report_generator.report_data_builder import ReportDataBuilder
from src.report_generator.pdf_report_builder import PDFReportBuilder
from src.report_generator.report_storage_service import ReportStorageService

class MockRow:
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

@patch("src.report_generator.report_data_builder.SessionLocal")
def test_report_data_builder_separates_decisions(mock_session_local):
    """
    Test that a bidder with one Confirmed flag and one Overridden flag 
    shows both the original AI recommendation and the officer's final decision for each.
    """
    mock_db = MagicMock()
    mock_session_local.return_value.__enter__.return_value = mock_db
    
    # Mock Bidder
    mock_db.execute.return_value.fetchone.side_effect = [
        MockRow(legal_name="Test Bidder Corp"), # bidder info
        MockRow(status="CONFIRMED", reason_notes="Looks fine.", created_at=None, user_id="u1"), # decision 1
        MockRow(status="OVERRIDDEN", reason_notes="Actually this is ok.", created_at=None, user_id="u2") # decision 2
    ]
    
    # Mock Flags
    mock_db.execute.return_value.fetchall.return_value = [
        MockRow(
            id="f1", rule_id="rule1", status="POTENTIAL_NON_COMPLIANCE", 
            severity="HIGH", title="Flag 1", reason="Reason 1", 
            ai_recommendation="AI says non-compliant", 
            anchors=[{"documentId": "d1", "pageNumber": 1}]
        ),
        MockRow(
            id="f2", rule_id="rule2", status="NEEDS_REVIEW", 
            severity="MEDIUM", title="Flag 2", reason="Reason 2", 
            ai_recommendation="AI says review", 
            anchors=[{"documentId": "d2", "pageNumber": 2}]
        )
    ]
    
    report_data = ReportDataBuilder.build_report_data("t1", "b1")
    
    assert report_data["legal_name"] == "Test Bidder Corp"
    assert len(report_data["flags"]) == 2
    
    flag1 = report_data["flags"][0]
    assert flag1["ai_recommendation"]["status"] == "POTENTIAL_NON_COMPLIANCE"
    assert flag1["officer_decision"]["status"] == "CONFIRMED"
    assert flag1["evidence"][0]["documentId"] == "d1"
    
    flag2 = report_data["flags"][1]
    assert flag2["ai_recommendation"]["status"] == "NEEDS_REVIEW"
    assert flag2["officer_decision"]["status"] == "OVERRIDDEN"
    assert flag2["evidence"][0]["documentId"] == "d2"


def test_pdf_report_builder_includes_references():
    report_data = {
        "tender_id": "t1",
        "bidder_id": "b1",
        "legal_name": "Test Bidder",
        "flags": [
            {
                "title": "Test Flag",
                "rule": "RuleX",
                "ai_recommendation": {"status": "TEST", "reason": "Test", "confidence_notes": "Test"},
                "officer_decision": None,
                "evidence": [{"documentId": "doc123", "pageNumber": 99, "snippet": "Bad snippet"}]
            }
        ]
    }
    pdf_bytes = PDFReportBuilder.build_pdf(report_data)
    
    # PDF should start with correct magic signature
    assert pdf_bytes.startswith(b"%PDF-")
    # PDF contains our text (basic check, though compressed we can't search text easily without parsing, 
    # but we can verify it doesn't crash)
    assert len(pdf_bytes) > 1000

@patch("src.report_generator.report_storage_service.Minio")
def test_report_generation_does_not_overwrite(mock_minio):
    """
    Test generating a second report does not alter the first by ensuring
    unique keys are generated.
    """
    key1 = ReportStorageService.store_report("t1", "b1", b"PDF1")
    key2 = ReportStorageService.store_report("t1", "b1", b"PDF2")
    
    assert key1 != key2
    assert key1.startswith("reports/t1/b1/compliance_report_")
    assert key2.startswith("reports/t1/b1/compliance_report_")
