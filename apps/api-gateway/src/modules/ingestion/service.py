import os
import uuid
from typing import Optional
from fastapi import UploadFile, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.database.models.document import DocumentModel, ProcessingJobModel
from src.storage.object_storage_adapter import ObjectStorageAdapter
from src.events.publishers.document_events import publish_document_uploaded
from src.modules.ingestion.schemas import DocumentUploadResponse, ProcessingJobResponse
from govflow_shared_types import ProcessingJob

ALLOWED_EXTENSIONS = {".pdf", ".png", ".jpg", ".jpeg", ".zip"}
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50 MB

_storage_adapter = None

def get_storage_adapter():
    global _storage_adapter
    if _storage_adapter is None:
        _storage_adapter = ObjectStorageAdapter()
    return _storage_adapter

async def upload_document(
    tender_id: str,
    file: UploadFile,
    db: AsyncSession,
    bidder_id: Optional[str] = None,
) -> DocumentUploadResponse:
    # 1. Validation
    _, ext = os.path.splitext(file.filename)
    if ext.lower() not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type. Allowed: {', '.join(ALLOWED_EXTENSIONS)}"
        )
    
    file_bytes = await file.read()
    if len(file_bytes) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=400,
            detail="File size exceeds the 50MB limit."
        )

    # 2. Upload to MinIO
    doc_id = str(uuid.uuid4())
    storage_path = f"tenders/{tender_id}/{doc_id}{ext}"
    try:
        get_storage_adapter().upload_file(storage_path, file_bytes, file.content_type)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to upload file to storage.")

    # 3. Create DB Records
    new_doc = DocumentModel(
        id=doc_id,
        tender_id=tender_id,
        bidder_id=bidder_id,
        file_name=file.filename,
        file_size=len(file_bytes),
        file_type=file.content_type,
        storage_path=storage_path,
        status="uploaded"
    )
    db.add(new_doc)

    job_id = str(uuid.uuid4())
    new_job = ProcessingJobModel(
        id=job_id,
        tender_id=tender_id,
        bidder_id=bidder_id,
        document_id=doc_id,
        job_type="ingestion",
        status="queued",
        progress=0.0
    )
    db.add(new_job)

    try:
        await db.commit()
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail="Database transaction failed.")

    # 4. Trigger Celery Task
    publish_document_uploaded(tender_id, doc_id, job_id)

    return DocumentUploadResponse(
        tender_id=tender_id,
        bidder_id=bidder_id,
        job_id=job_id,
        status="queued",
        message="Document uploaded and processing job queued successfully."
    )


async def get_processing_job(job_id: str, db: AsyncSession) -> ProcessingJobResponse:
    result = await db.execute(
        select(ProcessingJobModel).where(ProcessingJobModel.id == job_id)
    )
    job = result.scalar_one_or_none()
    
    if not job:
        raise HTTPException(status_code=404, detail="Processing job not found.")
        
    return ProcessingJobResponse(
        job=ProcessingJob.model_validate(job, from_attributes=True)
    )
