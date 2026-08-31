import pytest
from httpx import AsyncClient
from src.main import app

@pytest.mark.asyncio
async def test_get_extracted_fields():
    # Since we lack a fully isolated DB fixture in this stub test environment,
    # we mock the service method directly to ensure the schema formatting and routing works.
    from unittest.mock import patch
    from govflow_shared_types import ExtractedField, BoundingBox

    mock_field = ExtractedField(
        id="test-field-1",
        documentId="test-doc-123",
        pageNumber=1,
        fieldName="GSTIN",
        rawText="27ABCDE1234F1Z5",
        normalizedValue="27ABCDE1234F1Z5",
        confidence=0.98,
        boundingBox=BoundingBox(
            pageNumber=1,
            pageWidth=800.0,
            pageHeight=1000.0,
            x1=10.0,
            y1=20.0,
            x2=100.0,
            y2=50.0
        ),
        extractionMethod="TestOCR",
        createdAt="2026-08-31T00:00:00Z"
    )

    with patch("src.modules.extraction.service.ExtractionService.get_extracted_fields") as mock_get:
        # Note: the endpoint does not filter out low confidence.
        # We test that it correctly returns exactly what is passed up from the repo.
        mock_get.return_value = [mock_field]

        async with AsyncClient(app=app, base_url="http://test") as ac:
            response = await ac.get("/documents/test-doc-123/extracted-fields")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["documentId"] == "test-doc-123"
        assert data[0]["fieldName"] == "GSTIN"
        assert data[0]["confidence"] == 0.98
        # Ensure BoundingBox contract is honored
        assert "boundingBox" in data[0]
        assert data[0]["boundingBox"]["x1"] == 10.0
        assert data[0]["boundingBox"]["pageWidth"] == 800.0
