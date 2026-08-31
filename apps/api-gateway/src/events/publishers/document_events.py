from src.events.celery_client import celery_app


def publish_document_uploaded(tender_id: str, document_id: str, job_id: str):
    """
    Publish document.uploaded event to the AI workers via Celery.
    """
    event_data = {
        "tender_id": tender_id,
        "document_id": document_id,
        "job_id": job_id,
        "timestamp": "now",  # Let worker handle actual timestamp conversion
    }
    
    celery_app.send_task(
        "ingestion.process_document_upload",
        kwargs={"event_data": event_data},
    )
    print(f"Published document.uploaded event for doc {document_id}")
