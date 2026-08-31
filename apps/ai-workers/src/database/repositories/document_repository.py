"""
GovFlow Document and ProcessingJob Database Repository
Handles persistence of Document, DocumentPage, and ProcessingJob records.
Converts ORM entities to authoritative Pydantic models from govflow_shared_types.
"""

from datetime import datetime, timezone
from typing import List, Optional
import uuid

from sqlalchemy.orm import Session
from govflow_shared_types import Document, DocumentPage, ProcessingJob

from src.database.models.document import (
    DocumentModel,
    DocumentPageModel,
    ProcessingJobModel,
)


def _dto_from_doc_model(row: DocumentModel) -> Document:
    return Document(
        id=row.id,
        tender_id=row.tender_id,
        bidder_id=row.bidder_id,
        required_document_id=row.required_document_id,
        document_type=row.document_type,
        file_name=row.file_name,
        file_size=row.file_size,
        file_type=row.file_type,
        storage_path=row.storage_path,
        page_count=row.page_count,
        status=row.status,
        error_message=row.error_message,
        created_at=row.created_at.isoformat() if row.created_at else datetime.now(timezone.utc).isoformat(),
        updated_at=row.updated_at.isoformat() if row.updated_at else datetime.now(timezone.utc).isoformat(),
    )


def _dto_from_page_model(row: DocumentPageModel) -> DocumentPage:
    return DocumentPage(
        id=row.id,
        document_id=row.document_id,
        page_number=row.page_number,
        page_width=row.page_width,
        page_height=row.page_height,
        image_storage_path=row.image_storage_path,
        created_at=row.created_at.isoformat() if row.created_at else datetime.now(timezone.utc).isoformat(),
    )


class DocumentRepository:
    def __init__(self, session: Session):
        self.session = session

    def save_document(
        self,
        *,
        document_id: Optional[str] = None,
        tender_id: str,
        bidder_id: str,
        file_name: str,
        file_size: int,
        file_type: str,
        storage_path: str,
        page_count: int = 0,
        document_type: Optional[str] = None,
        status: str = "uploaded",
        error_message: Optional[str] = None,
    ) -> Document:
        doc_id = document_id or str(uuid.uuid4())
        doc = self.session.query(DocumentModel).filter_by(id=doc_id).first()

        if doc is None:
            doc = DocumentModel(
                id=doc_id,
                tender_id=tender_id,
                bidder_id=bidder_id,
                file_name=file_name,
                file_size=file_size,
                file_type=file_type,
                storage_path=storage_path,
                page_count=page_count,
                document_type=document_type,
                status=status,
                error_message=error_message,
            )
            self.session.add(doc)
        else:
            doc.tender_id = tender_id
            doc.bidder_id = bidder_id
            doc.file_name = file_name
            doc.file_size = file_size
            doc.file_type = file_type
            doc.storage_path = storage_path
            doc.page_count = page_count
            if document_type:
                doc.document_type = document_type
            doc.status = status
            doc.error_message = error_message

        self.session.commit()
        self.session.refresh(doc)
        return _dto_from_doc_model(doc)

    def save_document_pages(
        self,
        document_id: str,
        pages_data: List[dict],
    ) -> List[DocumentPage]:
        created_pages: List[DocumentPage] = []

        for p_data in pages_data:
            page_id = p_data.get("id") or str(uuid.uuid4())
            page_model = DocumentPageModel(
                id=page_id,
                document_id=document_id,
                page_number=p_data["page_number"],
                page_width=p_data["page_width"],
                page_height=p_data["page_height"],
                image_storage_path=p_data.get("image_storage_path"),
            )
            self.session.add(page_model)
            self.session.flush()
            created_pages.append(_dto_from_page_model(page_model))

        self.session.commit()
        return created_pages

    def update_job_status(
        self,
        job_id: str,
        status: str,
        progress: float = 0.0,
        current_step: Optional[str] = None,
        error_message: Optional[str] = None,
    ) -> None:
        job = self.session.query(ProcessingJobModel).filter_by(id=job_id).first()
        if job:
            job.status = status
            job.progress = progress
            if current_step:
                job.current_step = current_step
            if error_message:
                job.error_message = error_message
            if status in ("completed", "failed"):
                job.completed_at = datetime.now(timezone.utc)
            self.session.commit()
