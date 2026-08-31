from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.session import get_db
from src.modules.auth.dependencies import get_current_active_user
from src.database.models.user import UserModel
from src.modules.graph.schemas import GraphResponse
from src.modules.graph.service import GraphService

router = APIRouter(prefix="/graph", tags=["graph"])

@router.get("/tenders/{tender_id}/bidders/{bidder_id}", response_model=GraphResponse)
async def get_bidder_graph(
    tender_id: str, 
    bidder_id: str, 
    db: AsyncSession = Depends(get_db),
    user: UserModel = Depends(get_current_active_user)
):
    """
    Retrieve the star-topology compliance graph for a bidder.
    Documents act as satellite nodes.
    """
    try:
        return await GraphService.get_bidder_graph(db, tender_id, bidder_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
