from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.database.models.extracted_field import ExtractedFieldModel

class ExtractionRepository:
    """Repository for querying ExtractedField records from the database."""

    @staticmethod
    async def get_extracted_fields_by_document(
        db: AsyncSession, 
        document_id: str, 
        page_number: Optional[int] = None
    ) -> List[ExtractedFieldModel]:
        """
        Retrieves extracted fields for a given document.
        Does NOT filter out low-confidence results, as they are needed for the Evidence Viewer.
        """
        stmt = select(ExtractedFieldModel).where(ExtractedFieldModel.document_id == document_id)
        
        if page_number is not None:
            stmt = stmt.where(ExtractedFieldModel.page_number == page_number)
            
        stmt = stmt.order_by(ExtractedFieldModel.page_number, ExtractedFieldModel.field_name)
        
        result = await db.execute(stmt)
        return result.scalars().all()
