import pytest
from httpx import AsyncClient
from src.main import app
from src.database.models.report import ReportStatus

@pytest.mark.asyncio
async def test_trigger_report_rbac(async_client: AsyncClient, get_token_for_role):
    # Test unauthorized role
    token = get_token_for_role("Tender Committee Member")
    response = await async_client.post(
        "/tenders/t1/bidders/b1/reports",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 403
    
    # Test authorized role
    token = get_token_for_role("Procurement Officer")
    response = await async_client.post(
        "/tenders/t1/bidders/b1/reports",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == ReportStatus.PENDING.value
    assert data["tender_id"] == "t1"
    assert data["bidder_id"] == "b1"
    
    # Trigger again, should create a second unique report
    response2 = await async_client.post(
        "/tenders/t1/bidders/b1/reports",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response2.status_code == 200
    data2 = response2.json()
    assert data2["id"] != data["id"] # Two unique reports generated

@pytest.mark.asyncio
async def test_get_reports(async_client: AsyncClient, get_token_for_role):
    token = get_token_for_role("Procurement Officer")
    
    # Create one report
    await async_client.post(
        "/tenders/t2/bidders/b2/reports",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    # Test getting reports as auditor
    token_auditor = get_token_for_role("Compliance Auditor")
    response = await async_client.get(
        "/tenders/t2/bidders/b2/reports",
        headers={"Authorization": f"Bearer {token_auditor}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    
    # Since it's PENDING, no download URL should be present
    assert data[0]["download_url"] is None
