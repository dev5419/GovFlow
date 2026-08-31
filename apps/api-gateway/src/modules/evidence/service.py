from typing import List, Dict, Any, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Request

from govflow_shared_types import ExtractedField, EvidenceAnchor, BoundingBox
from src.modules.evidence.repository import EvidenceRepository
from src.modules.evidence.schemas import SignedUrlResponse, EvidenceOverlayResponse, LinkedEvidenceResponse
from src.modules.ingestion.signed_url_service import generate_presigned_url

class EvidenceService:
    
    @staticmethod
    def _get_client_info(request: Request) -> tuple[str, str]:
        ip = request.client.host if request.client else "unknown"
        ua = request.headers.get("user-agent", "unknown")
        return ip, ua

    @staticmethod
    async def get_document_url(
        db: AsyncSession, 
        document_id: str, 
        page_number: int, 
        user_id: str,
        request: Request
    ) -> SignedUrlResponse:
        """
        Returns a temporary signed URL for viewing the document image/PDF.
        """
        # In a real MinIO implementation, the object key might include the page number or just the doc ID.
        object_key = f"documents/{document_id}/page_{page_number}.png"
        url = generate_presigned_url("govflow-documents", object_key, expires_in=3600)
        
        # Log access
        ip, ua = EvidenceService._get_client_info(request)
        await EvidenceRepository.log_access(db, user_id, "DOCUMENT_URL", document_id, ip, ua)
        
        # Mocking expiry timestamp for response (current time + 3600)
        import time
        expires_at = int(time.time()) + 3600
        
        return SignedUrlResponse(
            url=url,
            expires_at=expires_at,
            document_id=document_id,
            page_number=page_number
        )

    @staticmethod
    async def get_overlays(
        db: AsyncSession,
        tender_id: str,
        bidder_id: str,
        document_id: str,
        page_number: int,
        user_id: str,
        request: Request
    ) -> EvidenceOverlayResponse:
        """
        Aggregates AI Extracted Fields and Compliance Evidence Anchors for a single page.
        """
        fields_db = await EvidenceRepository.get_fields_for_page(db, document_id, page_number)
        
        # Map fields to govflow_shared_types.ExtractedField
        mapped_fields = []
        for f in fields_db:
            mapped_fields.append(
                ExtractedField(
                    canonical_name=f.canonical_name,
                    raw_value=f.raw_value,
                    confidence=f.confidence,
                    bounding_box=BoundingBox(**f.bounding_box) if f.bounding_box else None,
                    page_number=f.page_number
                )
            )
            
        flags_db = await EvidenceRepository.get_flags_by_bidder(db, tender_id, bidder_id)
        
        mapped_anchors = []
        for flag in flags_db:
            for anchor_data in flag.anchors:
                if anchor_data.get("documentId") == document_id and anchor_data.get("pageNumber") == page_number:
                    mapped_anchors.append(EvidenceAnchor(**anchor_data))

        # Log access
        ip, ua = EvidenceService._get_client_info(request)
        await EvidenceRepository.log_access(db, user_id, "EVIDENCE_OVERLAY", f"{document_id}:{page_number}", ip, ua)

        return EvidenceOverlayResponse(
            document_id=document_id,
            page_number=page_number,
            fields=mapped_fields,
            anchors=mapped_anchors
        )

    @staticmethod
    async def get_linked_evidence(
        db: AsyncSession,
        flag_id: str,
        source_anchor_id: str,
        user_id: str,
        request: Request
    ) -> LinkedEvidenceResponse:
        """
        Resolves the "other side" of a contradiction given one anchor.
        """
        flag = await EvidenceRepository.get_flag_by_id(db, flag_id)
        if not flag:
            raise ValueError("Flag not found")
            
        linked_anchors = []
        for anchor_data in flag.anchors:
            if anchor_data.get("id") != source_anchor_id:
                linked_anchors.append(EvidenceAnchor(**anchor_data))
                
        # Log access
        ip, ua = EvidenceService._get_client_info(request)
        await EvidenceRepository.log_access(db, user_id, "LINKED_EVIDENCE", flag_id, ip, ua)
        
        return LinkedEvidenceResponse(
            source_anchor_id=source_anchor_id,
            linked_anchors=linked_anchors
        )
