import pytest
from src.modules.graph.status_resolver import resolve_node_status
from fastapi.testclient import TestClient
from src.main import app
from src.modules.auth.dependencies import get_current_active_user
from src.database.models.user import UserModel
from unittest.mock import patch, AsyncMock
from src.database.models.bidder import BidderModel
from src.database.models.document import DocumentModel, ProcessingJobModel

# ---------------------------------------------------------
# 1. Test Priority Cascade (Unit Tests for Resolver)
# ---------------------------------------------------------

def test_priority_processing_beats_all():
    # If a document has a "PROCESSING" job, it stays PROCESSING even if a previous run produced a VERIFIED flag
    status = resolve_node_status("PROCESSING", ["VERIFIED"])
    assert status == "PROCESSING"

def test_priority_missing_beats_non_compliance():
    status = resolve_node_status("MISSING", ["POTENTIAL_NON_COMPLIANCE"])
    assert status == "MISSING"

def test_priority_non_compliance_beats_review():
    status = resolve_node_status("COMPLETED", ["NEEDS_REVIEW", "POTENTIAL_NON_COMPLIANCE"])
    assert status == "POTENTIAL_NON_COMPLIANCE"

def test_priority_review_beats_verified():
    status = resolve_node_status("COMPLETED", ["VERIFIED", "VERIFIED", "NEEDS_REVIEW"])
    assert status == "NEEDS_REVIEW"

def test_no_flags_and_completed_is_verified():
    status = resolve_node_status("COMPLETED", [])
    assert status == "VERIFIED"


# ---------------------------------------------------------
# 2. Test Missing Node Generation (API Integration)
# ---------------------------------------------------------

client = TestClient(app)

def override_active_user():
    return UserModel(id="u1", role="Compliance Auditor")

@pytest.fixture
def auth_overrides():
    app.dependency_overrides[get_current_active_user] = override_active_user
    yield
    app.dependency_overrides = {}


@pytest.mark.asyncio
async def test_graph_generates_missing_nodes(auth_overrides):
    # Mocking the repository to return 0 documents for a tender that requires 3 documents
    
    mock_bidder = BidderModel(id="b1", legal_name="Acme Corp")
    
    with patch("src.modules.graph.repository.GraphRepository.get_bidder", new_callable=AsyncMock) as m_bidder:
        m_bidder.return_value = mock_bidder
        with patch("src.modules.graph.repository.GraphRepository.get_documents_by_bidder", new_callable=AsyncMock) as m_docs:
            m_docs.return_value = [] # ZERO uploaded documents
            
            with patch("src.modules.graph.repository.GraphRepository.get_tender_requirements", new_callable=AsyncMock) as m_reqs:
                # 3 requirements
                m_reqs.return_value = ["GST_CERTIFICATE", "PAN_CARD", "FINANCIAL_STATEMENT"]
                
                response = client.get("/graph/tenders/t1/bidders/b1")
                assert response.status_code == 200
                data = response.json()
                
                nodes = data["nodes"]
                edges = data["edges"]
                
                # 1 bidder + 3 missing docs = 4 nodes
                assert len(nodes) == 4
                # 3 edges connecting bidder to missing docs
                assert len(edges) == 3
                
                # Check statuses
                doc_nodes = [n for n in nodes if n["type"] == "DOCUMENT"]
                for n in doc_nodes:
                    assert n["status"] == "MISSING"
                    assert n["id"].startswith("missing-")
