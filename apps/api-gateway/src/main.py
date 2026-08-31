from fastapi import FastAPI

from src.modules.auth.router import router as auth_router
from src.modules.tenders.router import router as tenders_router
from src.modules.bidders.router import router as bidders_router
from src.modules.ingestion.router import router as ingestion_router
from src.modules.documents.router import router as documents_router
from src.modules.extraction.router import router as extraction_router
from src.modules.compliance.router import router as compliance_router
from src.modules.graph.router import router as graph_router
from src.modules.evidence.router import router as evidence_router
from src.modules.reports.router import router as reports_router
from src.modules.audit.router import router as audit_router
import asyncio
from src.events.redis_subscriber import start_redis_subscribers

app = FastAPI(title="GovFlow API Gateway", version="0.1.0")

app.include_router(auth_router)
app.include_router(tenders_router)
app.include_router(bidders_router)
app.include_router(ingestion_router)
app.include_router(documents_router)
app.include_router(extraction_router)
app.include_router(compliance_router)
app.include_router(graph_router)
app.include_router(evidence_router)
app.include_router(reports_router)
app.include_router(audit_router)


@app.get("/health")
async def health():
    return {"status": "ok"}

@app.on_event("startup")
async def startup_event():
    # Start the redis subscriber in the background
    asyncio.create_task(start_redis_subscribers())
