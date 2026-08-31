from fastapi import APIRouter, Depends, Request, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.session import get_db
from src.modules.auth.dependencies import get_current_active_user
from src.database.models.user import UserModel
from src.modules.evidence.schemas import SignedUrlResponse, EvidenceOverlayResponse, LinkedEvidenceResponse
from src.modules.evidence.service import EvidenceService

router = APIRouter(prefix="/evidence", tags=["evidence"])

@router.get("/documents/{document_id}/pages/{page_number}/url", response_model=SignedUrlResponse)
async def get_document_url(
    document_id: str,
    page_number: int,
    request: Request,
    db: AsyncSession = Depends(get_db),
    user: UserModel = Depends(get_current_active_user)
):
    """
    Get a temporary signed URL for viewing a document page image.
    Never returns a public or permanent URL. All accesses are audited.
    """
    return await EvidenceService.get_document_url(db, document_id, page_number, user.id, request)

@router.get("/overlays/tenders/{tender_id}/bidders/{bidder_id}/documents/{document_id}/pages/{page_number}", response_model=EvidenceOverlayResponse)
async def get_evidence_overlays(
    tender_id: str,
    bidder_id: str,
    document_id: str,
    page_number: int,
    request: Request,
    db: AsyncSession = Depends(get_db),
    user: UserModel = Depends(get_current_active_user)
):
    """
    Get all extracted fields and compliance evidence anchors for a specific document page.
    All accesses are audited.
    """
    return await EvidenceService.get_overlays(
        db=db,
        tender_id=tender_id,
        bidder_id=bidder_id,
        document_id=document_id,
        page_number=page_number,
        user_id=user.id,
        request=request
    )

@router.get("/flags/{flag_id}/anchors/{anchor_id}/linked", response_model=LinkedEvidenceResponse)
async def get_linked_evidence(
    flag_id: str,
    anchor_id: str,
    request: Request,
    db: AsyncSession = Depends(get_db),
    user: UserModel = Depends(get_current_active_user)
):
    """
    Resolve 'linked evidence' for a given contradiction anchor.
    Returns the opposing side(s) of the contradiction. All accesses are audited.
    """
    try:
        return await EvidenceService.get_linked_evidence(db, flag_id, anchor_id, user.id, request)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
