from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from src.modules.extraction.repository import ExtractionRepository
from govflow_shared_types import ExtractedField

class ExtractionService:
    """Service for handling extraction-related business logic."""

    @staticmethod
    async def get_extracted_fields(
        db: AsyncSession, 
        document_id: str, 
        page_number: Optional[int] = None
    ) -> List[ExtractedField]:
        """
        Retrieves extracted fields for a document and maps them to the Pydantic schema.
        """
        orm_fields = await ExtractionRepository.get_extracted_fields_by_document(
            db=db, 
            document_id=document_id, 
            page_number=page_number
        )

        return [
            ExtractedField.model_validate(
                {
                    "id": field.id,
                    "documentId": field.document_id,
                    "pageNumber": field.page_number,
                    "fieldName": field.field_name,
                    "rawText": field.raw_text,
                    "normalizedValue": field.normalized_value,
                    "confidence": field.confidence,
                    "boundingBox": field.bounding_box, # JSONB automatically parses to dict in SQLAlchemy
                    "extractionMethod": field.extraction_method,
                    "createdAt": field.created_at.isoformat() if hasattr(field.created_at, "isoformat") else str(field.created_at)
                }
            )
            for field in orm_fields
        ]
