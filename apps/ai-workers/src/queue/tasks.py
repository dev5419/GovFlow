"""
GovFlow Celery Tasks Initialization and Registration.
Broker and result backend configured with Redis per techstack.md.
"""

from typing import Any, Dict, List, Optional
from celery import Celery
from src.shared.config import settings
from src.database import get_db_session
from src.queue.consumers.ingestion_consumer import process_document_uploaded_event
from src.ocr.tasks import process_document_preprocessed_event

celery_app = Celery(
    "govflow_workers",
    broker=settings.redis_url,
    backend=settings.redis_url,
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
)

# Standard alias for Celery CLI auto-discovery
app = celery_app


@celery_app.task(name="ingestion.process_document_upload", bind=True)
def process_document_upload_task(
    self,
    event_data: Dict[str, Any],
    file_bytes: Optional[bytes] = None,
    file_path: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """
    Celery task consuming 'document.uploaded' event.
    Executes ingestion pipeline and emits 'document.preprocessed'.
    """
    with next(get_db_session()) as db_session:
        return process_document_uploaded_event(
            event_data=event_data,
            file_bytes=file_bytes,
            file_path=file_path,
            db_session=db_session,
        )

@celery_app.task(name="ocr.process_ocr_extraction", bind=True)
def process_ocr_extraction_task(
    self,
    event_data: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Celery task consuming 'document.preprocessed' event.
    Executes OCR and layout-aware extraction, saves ExtractedField records,
    and emits 'document.extraction.completed'.
    """
    with next(get_db_session()) as db_session:
        return process_document_preprocessed_event(
            event_data=event_data,
            db_session=db_session
        )
