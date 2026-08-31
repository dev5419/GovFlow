import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock
from src.main import app
from src.modules.auth.dependencies import get_current_active_user
from src.database.models.user import UserModel
from src.database.models.compliance_flag import ComplianceFlagModel
from src.database.models.extracted_field import ExtractedFieldModel

client = TestClient(app)

def override_active_user():
    return UserModel(id="u1", role="Procurement Officer")

@pytest.fixture
def auth_overrides():
    app.dependency_overrides[get_current_active_user] = override_active_user
    yield
    app.dependency_overrides = {}


@pytest.mark.asyncio
async def test_signed_url_expiration(auth_overrides):
    with patch("src.modules.evidence.repository.EvidenceRepository.log_access", new_callable=AsyncMock) as m_log:
        response = client.get("/evidence/documents/d1/pages/1/url")
        assert response.status_code == 200
        data = response.json()
        assert "url" in data
        assert "expires_at" in data
        # Ensure it expires in roughly 3600 seconds
        import time
        assert data["expires_at"] > time.time()
        assert m_log.called

@pytest.mark.asyncio
async def test_evidence_overlays_shape(auth_overrides):
    mock_field = ExtractedFieldModel(
        canonical_name="GSTIN",
        raw_value="12ABCDE3456F7Z8",
        confidence=0.9,
        bounding_box={"x0": 10, "y0": 20, "x1": 100, "y1": 40, "pageWidth": 1200, "pageHeight": 1600},
        page_number=1,
        document_id="d1"
    )
    
    mock_flag = ComplianceFlagModel(
        id="f1",
        tender_id="t1",
        bidder_id="b1",
        rule_name="gstin_match",
        status="POTENTIAL_NON_COMPLIANCE",
        reason="GSTIN mismatch",
        anchors=[
            {
                "id": "a1",
                "documentId": "d1",
                "pageNumber": 1,
                "boundingBox": {"x0": 10, "y0": 20, "x1": 100, "y1": 40, "pageWidth": 1200, "pageHeight": 1600},
                "snippet": "12ABCDE3456F7Z8",
                "confidence": 0.9
            }
        ]
    )

    with patch("src.modules.evidence.repository.EvidenceRepository.get_fields_for_page", new_callable=AsyncMock) as m_fields:
        m_fields.return_value = [mock_field]
        with patch("src.modules.evidence.repository.EvidenceRepository.get_flags_by_bidder", new_callable=AsyncMock) as m_flags:
            m_flags.return_value = [mock_flag]
            with patch("src.modules.evidence.repository.EvidenceRepository.log_access", new_callable=AsyncMock) as m_log:
                response = client.get("/evidence/overlays/tenders/t1/bidders/b1/documents/d1/pages/1")
                assert response.status_code == 200
                data = response.json()
                
                assert len(data["fields"]) == 1
                assert "pageWidth" in data["fields"][0]["bounding_box"]
                
                assert len(data["anchors"]) == 1
                assert "pageWidth" in data["anchors"][0]["boundingBox"]
                assert m_log.called

@pytest.mark.asyncio
async def test_linked_evidence_resolution(auth_overrides):
    mock_flag = ComplianceFlagModel(
        id="f1",
        tender_id="t1",
        bidder_id="b1",
        rule_name="gstin_match",
        status="POTENTIAL_NON_COMPLIANCE",
        reason="GSTIN mismatch",
        anchors=[
            {"id": "a1", "documentId": "d1", "pageNumber": 1, "boundingBox": {}, "snippet": "A", "confidence": 1.0},
            {"id": "a2", "documentId": "d2", "pageNumber": 1, "boundingBox": {}, "snippet": "B", "confidence": 1.0}
        ]
    )
    
    with patch("src.modules.evidence.repository.EvidenceRepository.get_flag_by_id", new_callable=AsyncMock) as m_flag:
        m_flag.return_value = mock_flag
        with patch("src.modules.evidence.repository.EvidenceRepository.log_access", new_callable=AsyncMock) as m_log:
            response = client.get("/evidence/flags/f1/anchors/a1/linked")
            assert response.status_code == 200
            data = response.json()
            assert data["source_anchor_id"] == "a1"
            assert len(data["linked_anchors"]) == 1
            assert data["linked_anchors"][0]["id"] == "a2"
            assert m_log.called
