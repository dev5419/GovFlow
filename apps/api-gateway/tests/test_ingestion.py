import pytest
import io
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock

from src.main import app

client = TestClient(app)


from src.database import get_db
from unittest.mock import AsyncMock

@pytest.fixture
def mock_db_session():
    mock_db = AsyncMock()
    app.dependency_overrides[get_db] = lambda: mock_db
    yield mock_db
    app.dependency_overrides.pop(get_db, None)


@pytest.fixture
def mock_storage():
    with patch("src.modules.ingestion.service.get_storage_adapter") as mock_adapter_func:
        mock_adapter = MagicMock()
        mock_adapter_func.return_value = mock_adapter
        yield mock_adapter


@pytest.fixture
def mock_publish():
    with patch("src.modules.ingestion.service.publish_document_uploaded") as mock_pub:
        yield mock_pub


def test_upload_invalid_extension(mock_storage, mock_publish, mock_db_session):
    # .exe is not allowed
    file_content = b"fake content"
    response = client.post(
        "/tenders/tender123/upload",
        files={"file": ("malicious.exe", file_content, "application/octet-stream")},
        data={"bidder_id": "bidder123"}
    )
    assert response.status_code == 400
    assert "Invalid file type" in response.json()["detail"]
    mock_storage.upload_file.assert_not_called()
    mock_publish.assert_not_called()


from src.database import get_db

@patch("src.modules.ingestion.service.AsyncSession")
def test_upload_valid_file(mock_async_session, mock_storage, mock_publish):
    # Mocking DB session
    mock_db = AsyncMock()
    app.dependency_overrides[get_db] = lambda: mock_db
    
    file_content = b"valid pdf content"
    response = client.post(
        "/tenders/tender123/upload",
        files={"file": ("doc.pdf", file_content, "application/pdf")},
        data={"bidder_id": "bidder123"}
    )
    
    assert response.status_code == 202
    data = response.json()
    assert data["tender_id"] == "tender123"
    assert data["bidder_id"] == "bidder123"
    assert "job_id" in data
    assert data["status"] == "queued"
    
    # Assert MinIO adapter was called
    mock_storage.upload_file.assert_called_once()
    
    # Assert celery publisher was called
    mock_publish.assert_called_once_with("tender123", mock_storage.upload_file.call_args[0][0].split('/')[2].replace('.pdf', ''), data["job_id"])


def test_upload_file_too_large(mock_storage, mock_publish, mock_db_session):
    # Max file size is 50MB
    # For testing, we mock the file.read() or just send a large file
    # We can mock file.read to return a large byte string
    
    with patch("starlette.datastructures.UploadFile.read", new_callable=AsyncMock, return_value=b"0" * (50 * 1024 * 1024 + 1)):
        response = client.post(
            "/tenders/tender123/upload",
            files={"file": ("doc.pdf", b"small", "application/pdf")},
            data={"bidder_id": "bidder123"}
        )
        assert response.status_code == 400
    assert "File size exceeds" in response.json()["detail"]
