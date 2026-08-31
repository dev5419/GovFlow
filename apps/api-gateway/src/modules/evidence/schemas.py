from typing import List, Optional
from pydantic import BaseModel, Field
from govflow_shared_types import ExtractedField, EvidenceAnchor

class SignedUrlResponse(BaseModel):
    url: str
    expires_at: int # Unix timestamp
    document_id: str
    page_number: int

class EvidenceOverlayResponse(BaseModel):
    document_id: str
    page_number: int
    fields: List[ExtractedField]
    anchors: List[EvidenceAnchor]

class LinkedEvidenceResponse(BaseModel):
    source_anchor_id: str
    linked_anchors: List[EvidenceAnchor]
