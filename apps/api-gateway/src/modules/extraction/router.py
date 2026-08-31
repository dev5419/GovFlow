from typing import List, Optional
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_db
from src.modules.extraction.service import ExtractionService
from govflow_shared_types import ExtractedField

router = APIRouter(prefix="/documents", tags=["Extraction"])

@router.get("/{document_id}/extracted-fields", response_model=List[ExtractedField])
async def get_extracted_fields(
    document_id: str,
    page_number: Optional[int] = Query(None, description="Filter fields by a specific page number"),
    db: AsyncSession = Depends(get_db)
):
    """
    Retrieve all extracted fields for a given document.
    Includes low-confidence fields and precise bounding boxes mapping directly
    to the Pydantic shared types contract.
    """
    fields = await ExtractionService.get_extracted_fields(
        db=db, 
        document_id=document_id, 
        page_number=page_number
    )
    
    if not fields and page_number is None:
        # In MVP, this could either return empty list or 404 if document not found.
        # Returning empty list is generally safer for querying incomplete extractions,
        # but let's assume empty list is valid.
        pass

    return fields
