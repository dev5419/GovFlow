from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.models.extracted_field import ExtractedFieldModel
import govflow_shared_types as shared_types

class ExtractionRepository:
    """Repository for saving ExtractedField records to the database."""

    @staticmethod
    async def save_extracted_fields(
        db: AsyncSession, 
        fields: List[shared_types.ExtractedField]
    ) -> None:
        """
        Saves a batch of extracted fields to the database.
        Maps the shared_types.ExtractedField Pydantic models to ORM models.
        """
        orm_fields = []
        for field in fields:
            orm_field = ExtractedFieldModel(
                id=field.id,
                document_id=field.document_id,
                page_number=field.page_number,
                field_name=field.field_name,
                raw_text=field.raw_text,
                normalized_value=field.normalized_value,
                confidence=field.confidence,
                bounding_box=field.bounding_box.model_dump(by_alias=True),
                extraction_method=field.extraction_method,
                # created_at is automatically set by the ORM
            )
            orm_fields.append(orm_field)

        db.add_all(orm_fields)
        await db.commit()
