import asyncio
from typing import Dict, Any
from sqlalchemy import select
from src.database import async_session_factory
from src.database.models.document import ProcessingJobModel

async def _update_processing_job(document_id: str):
    async with async_session_factory() as db_session:
        stmt = select(ProcessingJobModel).where(ProcessingJobModel.document_id == document_id)
        result = await db_session.execute(stmt)
        job = result.scalars().first()
        
        if job:
            job.current_step = "Extraction Completed"
            job.status = "processing"
            job.progress = 60.0
            db_session.add(job)
            await db_session.commit()

def handle_extraction_completed(event_data: Dict[str, Any]) -> None:
    """
    Handles the document.extraction.completed event.
    Updates the ProcessingJob to reflect that extraction is done and
    it is ready for the compliance evaluation phase.
    """
    document_id = event_data.get("documentId")
    if not document_id:
        return

    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
    loop.run_until_complete(_update_processing_job(document_id))
