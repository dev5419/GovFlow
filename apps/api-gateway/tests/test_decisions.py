import pytest
from fastapi.testclient import TestClient
from src.main import app
from src.modules.auth.dependencies import get_current_active_user, get_current_procurement_officer
from src.database.models.user import UserModel
from unittest.mock import patch, AsyncMock
from src.database.models.compliance_flag import ComplianceFlagModel

client = TestClient(app)

def override_active_user():
    return UserModel(id="u1", role="Compliance Auditor")

def override_proc_officer():
    return UserModel(id="u2", role="Procurement Officer")

@pytest.fixture
def auth_overrides():
    app.dependency_overrides[get_current_active_user] = override_active_user
    app.dependency_overrides[get_current_procurement_officer] = override_proc_officer
    yield
    app.dependency_overrides = {}

@pytest.fixture
def mock_db():
    with patch("src.modules.compliance.router.get_db") as mock:
        yield mock

def test_unauthorized_role_rejected(auth_overrides):
    # If a Compliance Auditor tries to use the endpoint, they should fail the procurement officer dependency.
    # To simulate this, we override get_current_procurement_officer to fail if the role isn't right.
    # Actually, our dependency `require_role(["Procurement Officer"])` raises HTTP 403.
    # Let's override the `get_current_active_user` that `require_role` uses under the hood.
    app.dependency_overrides.clear()
    
    # We mock the base active user to be an auditor
    app.dependency_overrides[get_current_active_user] = override_active_user
    
    response = client.post("/flags/f1/decisions", json={"decisionState": "Confirmed", "notes": ""})
    
    # Because get_current_procurement_officer calls require_role which calls get_current_active_user
    # it will see "Compliance Auditor" and raise 403.
    assert response.status_code == 403
    app.dependency_overrides.clear()

@pytest.mark.asyncio
async def test_record_decision_transaction():
    # Setup mock user as procurement officer
    app.dependency_overrides[get_current_active_user] = override_proc_officer
    
    mock_flag = ComplianceFlagModel(
        id="f1", tender_id="t1", bidder_id="b1", status="POTENTIAL_NON_COMPLIANCE", 
        severity="critical", title="Test", reason="Test", ai_recommendation="Test", anchors=[]
    )
    
    with patch("src.modules.compliance.repository.ComplianceRepository.get_flag_by_id", new_callable=AsyncMock) as mock_get_flag:
        mock_get_flag.return_value = mock_flag
        
        with patch("src.modules.compliance.repository.ComplianceRepository.record_decision", new_callable=AsyncMock) as mock_record:
            
            response = client.post("/flags/f1/decisions", json={"decisionState": "Overridden", "notes": "Approved."})
            
            assert response.status_code == 201
            mock_record.assert_called_once()
            
            # Assert flag was not modified before being passed to repository
            args, kwargs = mock_record.call_args
            passed_flag = args[1]
            assert passed_flag.status == "POTENTIAL_NON_COMPLIANCE" # Unchanged
    
    app.dependency_overrides.clear()
