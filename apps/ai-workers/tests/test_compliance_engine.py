import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from govflow_shared_types import ExtractedField, Document, TenderRule, RequiredDocument, ComplianceFlagStatus, BoundingBox, SeverityLevel
from src.compliance_engine.engine import ComplianceEngine

@pytest.mark.asyncio
async def test_compliance_engine_pipeline_gstin_mismatch():
    # Setup Fixtures matching PRD 8.4
    db_mock = AsyncMock()
    
    fields = [
        ExtractedField(
            id="field_1", 
            documentId="doc_1", 
            pageNumber=1, 
            fieldName="GSTIN", 
            rawText="27ABCDE1234F1Z5", 
            normalizedValue="27ABCDE1234F1Z5", 
            confidence=0.99, 
            extractionMethod="ocr", 
            createdAt="2026-01-01T00:00:00Z",
            boundingBox=BoundingBox(pageNumber=1, pageWidth=800, pageHeight=1000, x1=10, y1=10, x2=50, y2=20)
        ),
        ExtractedField(
            id="field_2", 
            documentId="doc_2", 
            pageNumber=1, 
            fieldName="GSTIN", 
            rawText="29ABCDE1234F1Z5", 
            normalizedValue="29ABCDE1234F1Z5", 
            confidence=0.95, 
            extractionMethod="ocr", 
            createdAt="2026-01-01T00:00:00Z",
            boundingBox=BoundingBox(pageNumber=1, pageWidth=800, pageHeight=1000, x1=10, y1=10, x2=50, y2=20)
        )
    ]
    
    documents = [
        Document(id="doc_1", tenderId="t1", bidderId="b1", fileName="gst.pdf", fileType="pdf", objectStoreKey="k1", documentType="GST Certificate", status="completed", createdAt="2026-01-01T00:00:00Z"),
        Document(id="doc_2", tenderId="t1", bidderId="b1", fileName="ca.pdf", fileType="pdf", objectStoreKey="k2", documentType="CA Certificate", status="completed", createdAt="2026-01-01T00:00:00Z")
    ]

    tender_rules = []
    required_documents = []

    # Ensure rule_registry knows about gstin_match
    # The rule modules should be imported to register them
    import src.compliance_engine.rules.gstin_match
    
    # We patch the repositories so we don't hit a real database
    with patch("src.compliance_engine.engine.ComplianceRepository.save_flags") as mock_save:
        with patch("src.compliance_engine.engine.ComplianceEngine._update_bidder_summary") as mock_summary:
            
            flags = await ComplianceEngine.evaluate(
                db=db_mock,
                extracted_fields=fields,
                documents=documents,
                tender_rules=tender_rules,
                required_documents=required_documents,
                tender_id="t1",
                bidder_id="b1"
            )
            
            # Assertions based on PRD §8.4 Acceptance Criteria
            # 1. Finds a mismatch
            mismatch_flag = next((f for f in flags if f.get("title") == "GSTIN Mismatch"), None)
            assert mismatch_flag is not None, "Failed to generate GSTIN Mismatch flag"
            
            # 2. Status is POTENTIAL_NON_COMPLIANCE (high confidence mismatch)
            assert mismatch_flag["status"] == ComplianceFlagStatus.POTENTIAL_NON_COMPLIANCE
            assert mismatch_flag["severity"] == SeverityLevel.CRITICAL
            
            # 3. Evidence links to BOTH source documents
            assert "anchors" in mismatch_flag
            anchors = mismatch_flag["anchors"]
            assert len(anchors) == 2
            
            doc_ids = [a.documentId for a in anchors]
            assert "doc_1" in doc_ids
            assert "doc_2" in doc_ids
            
            # 4. Reason string is non-empty and descriptive
            assert mismatch_flag["reason"]
            assert "doc_1" in mismatch_flag["reason"]
            assert "doc_2" in mismatch_flag["reason"]
            
            # 5. Must have a ruleId
            assert mismatch_flag["ruleId"]
            
            # 6. Check that save was called
            mock_save.assert_called_once()
