"""
GovFlow Ingestion Consumer & Pipeline
Consumes 'document.uploaded' events, runs safe ZIP extraction, PDF splitting,
document classification, and OpenCV/Pillow image preprocessing per PRD §8.2, §11.2, §11.3.
"""

import os
import uuid
from typing import Any, Dict, List, Optional
from sqlalchemy.orm import Session

from src.ingestion_worker.zip_extractor import safe_extract_zip, SUPPORTED_EXTENSIONS
from src.ingestion_worker.pdf_splitter import split_pdf
from src.ingestion_worker.document_classifier import classify_document
from src.ingestion_worker.image_preprocessor import preprocess_image
from src.database.repositories.document_repository import DocumentRepository
from src.queue.producers.event_publisher import publish_document_preprocessed


SUPPORTED_INGESTION_EXTS = {".pdf", ".png", ".jpg", ".jpeg", ".zip"}


class IngestionError(Exception):
    """Raised when ingestion or file processing fails."""
    pass


def process_document_uploaded_event(
    event_data: Dict[str, Any],
    file_bytes: Optional[bytes] = None,
    file_path: Optional[str] = None,
    db_session: Optional[Session] = None,
) -> List[Dict[str, Any]]:
    """
    Core ingestion processor:
    1. Validates file format against MVP supported list (.pdf, .png, .jpg, .jpeg, .zip).
    2. Runs ZIP extraction (if applicable) -> PDF splitting -> classification -> image preprocessing.
    3. Persists records to database.
    4. Publishes 'document.preprocessed' event for each resulting document.
    """
    payload = event_data.get("payload", {})
    tender_id = payload.get("tenderId")
    bidder_id = payload.get("bidderId", "")
    job_id = payload.get("jobId")
    doc_data = payload.get("document", {})

    if not tender_id:
        raise IngestionError("Missing required field 'tenderId' in document.uploaded event.")
    if not job_id:
        raise IngestionError("Missing required field 'jobId' in document.uploaded event.")

    file_name = doc_data.get("fileName") or doc_data.get("file_name") or os.path.basename(file_path or "uploaded_doc")
    storage_path = doc_data.get("storagePath") or doc_data.get("storage_path") or (file_path or f"documents/{tender_id}/{file_name}")
    doc_id = doc_data.get("id") or str(uuid.uuid4())

    _, ext = os.path.splitext(file_name.lower())

    repo = DocumentRepository(db_session) if db_session else None

    # Step 1: Reject unsupported file formats immediately per PRD §8.2
    if ext not in SUPPORTED_INGESTION_EXTS:
        error_msg = f"Unsupported file type '{ext}'. Supported formats are: {', '.join(sorted(SUPPORTED_INGESTION_EXTS))}"
        if repo:
            repo.update_job_status(job_id, status="failed", error_message=error_msg)
        raise IngestionError(error_msg)

    # Read binary bytes if not provided directly
    if file_bytes is None:
        if file_path and os.path.isfile(file_path):
            with open(file_path, "rb") as f:
                file_bytes = f.read()
        else:
            raise IngestionError(f"No document content provided for processing: {file_name}")

    published_events: List[Dict[str, Any]] = []

    # Step 2: Handle ZIP archive extraction
    if ext == ".zip":
        if repo:
            repo.update_job_status(job_id, status="processing", progress=0.2, current_step="Extracting ZIP archive")

        extracted_files = safe_extract_zip(file_bytes)
        supported_items = [f for f in extracted_files if f.is_supported]

        if not supported_items:
            error_msg = "ZIP archive contains no supported document files (.pdf, .png, .jpg, .jpeg)."
            if repo:
                repo.update_job_status(job_id, status="failed", error_message=error_msg)
            raise IngestionError(error_msg)

        total_items = len(supported_items)
        for i, item in enumerate(supported_items):
            sub_doc_id = str(uuid.uuid4())
            events = _process_single_file(
                tender_id=tender_id,
                bidder_id=bidder_id,
                job_id=job_id,
                document_id=sub_doc_id,
                file_name=item.file_name,
                file_bytes=item.file_bytes,
                storage_path=f"documents/{tender_id}/{sub_doc_id}/{item.file_name}",
                repo=repo,
            )
            published_events.extend(events)
            if repo:
                progress = 0.2 + (0.7 * ((i + 1) / total_items))
                repo.update_job_status(job_id, status="processing", progress=progress, current_step=f"Processed {item.file_name}")

    else:
        # Step 3: Handle direct single file (.pdf or image)
        events = _process_single_file(
            tender_id=tender_id,
            bidder_id=bidder_id,
            job_id=job_id,
            document_id=doc_id,
            file_name=file_name,
            file_bytes=file_bytes,
            storage_path=storage_path,
            repo=repo,
        )
        published_events.extend(events)

    if repo:
        repo.update_job_status(job_id, status="completed", progress=1.0, current_step="Ingestion completed")

    return published_events


def _process_single_file(
    *,
    tender_id: str,
    bidder_id: str,
    job_id: str,
    document_id: str,
    file_name: str,
    file_bytes: bytes,
    storage_path: str,
    repo: Optional[DocumentRepository],
) -> List[Dict[str, Any]]:
    """
    Process an individual PDF or image file:
    1. Classifies document category.
    2. Splits multipage PDF or pre-processes image.
    3. Persists records to database.
    4. Emits 'document.preprocessed' event.
    """
    _, ext = os.path.splitext(file_name.lower())
    clean_type = ext.lstrip(".")

    # Classify document
    classification = classify_document(file_name)

    pages_payload: List[Dict[str, Any]] = []

    if ext == ".pdf":
        split_pages = split_pdf(file_bytes)
        page_count = len(split_pages)

        for p in split_pages:
            pages_payload.append({
                "id": str(uuid.uuid4()),
                "documentId": document_id,
                "pageNumber": p.page_number,
                "pageWidth": p.page_width,
                "pageHeight": p.page_height,
                "imageStoragePath": f"{storage_path}/page_{p.page_number}.png",
                "createdAt": doc_now_iso(),
            })

    elif ext in (".png", ".jpg", ".jpeg"):
        prep = preprocess_image(file_bytes)
        page_count = 1
        pages_payload.append({
            "id": str(uuid.uuid4()),
            "documentId": document_id,
            "pageNumber": 1,
            "pageWidth": prep.width,
            "pageHeight": prep.height,
            "imageStoragePath": storage_path,
            "createdAt": doc_now_iso(),
        })
    else:
        raise IngestionError(f"Unsupported extension in single file pipeline: '{ext}'")

    # Persist in DB if repository is provided
    if repo:
        repo.save_document(
            document_id=document_id,
            tender_id=tender_id,
            bidder_id=bidder_id,
            file_name=file_name,
            file_size=len(file_bytes),
            file_type=clean_type,
            storage_path=storage_path,
            page_count=page_count,
            document_type=classification.document_type,
            status="preprocessed",
        )

        db_pages_data = [
            {
                "id": p["id"],
                "page_number": p["pageNumber"],
                "page_width": p["pageWidth"],
                "page_height": p["pageHeight"],
                "image_storage_path": p["imageStoragePath"],
            }
            for p in pages_payload
        ]
        repo.save_document_pages(document_id, db_pages_data)

    # Publish document.preprocessed event
    event = publish_document_preprocessed(
        tender_id=tender_id,
        bidder_id=bidder_id,
        document_id=document_id,
        job_id=job_id,
        pages=pages_payload,
    )

    return [event]


def doc_now_iso() -> str:
    from datetime import datetime, timezone
    return datetime.now(timezone.utc).isoformat()
