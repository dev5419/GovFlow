from typing import Dict, Any, List
from sqlalchemy.ext.asyncio import AsyncSession
from src.ocr.extraction_pipeline import ExtractionPipeline
from src.database.repositories.extraction_repository import ExtractionRepository
import govflow_shared_types as shared_types
import uuid
import datetime
import json

def process_document_preprocessed_event(
    event_data: Dict[str, Any],
    db_session: Any
) -> List[Dict[str, Any]]:
    """
    Consumes 'document.preprocessed' event and produces 'document.extraction.completed'.
    Orchestrates the OCR pipeline for all pages.
    """
    document_id = event_data.get("documentId")
    tender_id = event_data.get("tenderId")
    pages = event_data.get("pages", [])

    pipeline = ExtractionPipeline()
    repository = ExtractionRepository()
    
    all_extracted_fields = []
    
    for page in pages:
        page_number = page.get("pageNumber", 1)
        page_width = page.get("pageWidth", 1000)
        page_height = page.get("pageHeight", 1000)
        image_path = page.get("imageStoragePath", "")

        extracted_fields = pipeline.process_page(
            document_id=document_id,
            page_number=page_number,
            page_width=page_width,
            page_height=page_height,
            image_path=image_path
        )
        all_extracted_fields.extend(extracted_fields)

    # Save to database (Assuming db_session is sync or we run async function)
    import asyncio
    
    # Check if we need to run asyncio event loop for save_extracted_fields
    # For Celery tasks, we might be inside a sync function calling async.
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
    loop.run_until_complete(repository.save_extracted_fields(db_session, all_extracted_fields))

    # Publish document.extraction.completed event (Stubbed for MVP)
    event_payload = {
        "eventId": str(uuid.uuid4()),
        "eventType": "document.extraction.completed",
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "data": {
            "documentId": document_id,
            "tenderId": tender_id,
            "extractedFieldsCount": len(all_extracted_fields)
        }
    }
    
    # In a real system, publish to Redis/Kafka. Here we just return it.
    print(f"Published event: document.extraction.completed for doc {document_id}")
    return event_payload
