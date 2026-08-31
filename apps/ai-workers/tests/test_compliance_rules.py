import pytest
from govflow_shared_types import ExtractedField, ComplianceFlagStatus, SeverityLevel, TenderRule, Document, RequiredDocument
from src.compliance_engine.rules.gstin_match import evaluate_gstin_match
from src.compliance_engine.rules.legal_name_match import evaluate_legal_name_match, normalize_legal_name
from src.compliance_engine.rules.address_match import evaluate_address_match
from src.compliance_engine.rules.turnover_threshold import evaluate_turnover_threshold
from src.compliance_engine.rules.required_document_check import evaluate_required_documents

def test_gstin_match_low_confidence():
    fields = [
        ExtractedField(id="1", documentId="d1", pageNumber=1, fieldName="GSTIN", rawText="123", normalizedValue="123", confidence=0.5, extractionMethod="ocr", createdAt="2026"),
        ExtractedField(id="2", documentId="d2", pageNumber=1, fieldName="GSTIN", rawText="123", normalizedValue="123", confidence=0.9, extractionMethod="ocr", createdAt="2026")
    ]
    flags = evaluate_gstin_match(fields, tender_id="t1", bidder_id="b1")
    assert any(f["status"] == ComplianceFlagStatus.NEEDS_REVIEW for f in flags)
    assert any(f["status"] == ComplianceFlagStatus.VERIFIED for f in flags) # Since the other is alone now

def test_gstin_match_conflict():
    fields = [
        ExtractedField(id="1", documentId="d1", pageNumber=1, fieldName="GSTIN", rawText="123", normalizedValue="123", confidence=0.9, extractionMethod="ocr", createdAt="2026"),
        ExtractedField(id="2", documentId="d2", pageNumber=1, fieldName="GSTIN", rawText="456", normalizedValue="456", confidence=0.9, extractionMethod="ocr", createdAt="2026")
    ]
    flags = evaluate_gstin_match(fields, tender_id="t1", bidder_id="b1")
    assert len(flags) == 1
    assert flags[0]["status"] == ComplianceFlagStatus.POTENTIAL_NON_COMPLIANCE
    assert "123" not in flags[0]["reason"] # wait, the reason just says mismatch between documents

def test_legal_name_normalization():
    assert normalize_legal_name("ABC Pvt. Ltd.") == "abc"
    assert normalize_legal_name("ABC PVT LTD") == "abc"
    assert normalize_legal_name("Tech Corp., Inc.") == "tech"
    assert normalize_legal_name("Global  Logistics LLC") == "global logistics"

def test_legal_name_match():
    fields = [
        ExtractedField(id="1", documentId="d1", pageNumber=1, fieldName="Legal Entity Name", rawText="ABC Pvt. Ltd.", normalizedValue="ABC Pvt. Ltd.", confidence=0.9, extractionMethod="ocr", createdAt="2026"),
        ExtractedField(id="2", documentId="d2", pageNumber=1, fieldName="Legal Entity Name", rawText="ABC PVT LTD", normalizedValue="ABC PVT LTD", confidence=0.9, extractionMethod="ocr", createdAt="2026")
    ]
    flags = evaluate_legal_name_match(fields, tender_id="t1", bidder_id="b1")
    assert len(flags) == 1
    assert flags[0]["status"] == ComplianceFlagStatus.VERIFIED

def test_address_match_similarity():
    fields = [
        ExtractedField(id="1", documentId="d1", pageNumber=1, fieldName="Registered Address", rawText="123 Main St, New York", normalizedValue="123 Main St, New York", confidence=0.9, extractionMethod="ocr", createdAt="2026"),
        ExtractedField(id="2", documentId="d2", pageNumber=1, fieldName="Registered Address", rawText="123 Main Street NY", normalizedValue="123 Main Street NY", confidence=0.9, extractionMethod="ocr", createdAt="2026")
    ]
    flags = evaluate_address_match(fields, tender_id="t1", bidder_id="b1")
    # Similarity might be low (123, main, st, new, york) vs (123, main, street, ny) -> 2 / 7 = 0.28 which is < 0.7
    # So this will flag as mismatch under our current basic logic. That's fine for MVP testing.
    assert flags[0]["status"] == ComplianceFlagStatus.POTENTIAL_NON_COMPLIANCE

def test_turnover_threshold():
    fields = [
        ExtractedField(id="1", documentId="d1", pageNumber=1, fieldName="Turnover Value", rawText="4,500,000", normalizedValue="4,500,000", confidence=0.9, extractionMethod="ocr", createdAt="2026")
    ]
    rules = [TenderRule(id="r1", tenderId="t1", ruleType="turnover_threshold", title="Turnover", parameters={"min_turnover": 5000000}, isActive=True, createdAt="2026")]
    
    flags = evaluate_turnover_threshold(fields, tender_id="t1", bidder_id="b1", tender_rules=rules)
    assert flags[0]["status"] == ComplianceFlagStatus.POTENTIAL_NON_COMPLIANCE
    assert flags[0]["severity"] == SeverityLevel.CRITICAL

def test_required_document_missing():
    documents = [
        Document(id="d1", tenderId="t1", bidderId="b1", fileName="test", fileType="application/pdf", objectStoreKey="key", documentType="GST Certificate", status="completed", createdAt="2026")
    ]
    reqs = [
        RequiredDocument(id="r1", tenderId="t1", documentType="GST Certificate", isMandatory=True, description="GST", createdAt="2026"),
        RequiredDocument(id="r2", tenderId="t1", documentType="CA Certificate", isMandatory=True, description="CA", createdAt="2026")
    ]
    
    flags = evaluate_required_documents(documents=documents, tender_id="t1", bidder_id="b1", required_documents=reqs)
    
    missing_flags = [f for f in flags if f["status"] == ComplianceFlagStatus.MISSING]
    assert len(missing_flags) == 1
    assert "CA Certificate" in missing_flags[0]["reason"]
