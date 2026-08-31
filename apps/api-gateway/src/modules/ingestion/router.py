from typing import Optional
from fastapi import APIRouter, Depends, UploadFile, File, Form
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_db
from src.modules.ingestion import service
from src.modules.ingestion.schemas import DocumentUploadResponse, ProcessingJobResponse

router = APIRouter(prefix="", tags=["Ingestion"])

@router.post(
    "/tenders/{tender_id}/upload", 
    response_model=DocumentUploadResponse,
    status_code=202
)
async def upload_document(
    tender_id: str,
    file: UploadFile = File(...),
    bidder_id: Optional[str] = Form(None),
    db: AsyncSession = Depends(get_db)
):
    """
    Upload a document (PDF, Image, or ZIP) for a tender.
    Returns a tracking job ID.
    """
    return await service.upload_document(tender_id, file, db, bidder_id)


@router.get(
    "/jobs/{job_id}",
    response_model=ProcessingJobResponse
)
async def get_processing_job(
    job_id: str,
    db: AsyncSession = Depends(get_db)
):
    """
    Get the current status of an ingestion processing job.
    """
    return await service.get_processing_job(job_id, db)
