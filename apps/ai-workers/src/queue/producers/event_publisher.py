"""
GovFlow Queue Event Publisher
Publishes standardized asynchronous event payloads across worker modules per PRD §11.3.
"""

import json
import uuid
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
import redis

from src.shared.config import settings


def _get_redis_client():
    return redis.Redis.from_url(settings.redis_url, decode_responses=True)


def publish_document_preprocessed(
    *,
    tender_id: str,
    bidder_id: Optional[str],
    document_id: str,
    job_id: str,
    pages: List[Dict[str, Any]],
    correlation_id: Optional[str] = None,
    redis_client: Optional[redis.Redis] = None,
) -> Dict[str, Any]:
    """
    Constructs and emits the 'document.preprocessed' event payload per packages/api-contracts/events/document.preprocessed.json.
    """
    event_payload = {
        "eventId": str(uuid.uuid4()),
        "eventType": "document.preprocessed",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "correlationId": correlation_id or str(uuid.uuid4()),
        "payload": {
            "tenderId": tender_id,
            "bidderId": bidder_id or "",
            "documentId": document_id,
            "jobId": job_id,
            "pages": pages,
        },
    }

    try:
        r = redis_client or _get_redis_client()
        # Publish to Redis pub/sub channel and list queue for worker consumption
        event_json = json.dumps(event_payload)
        r.publish("events:document.preprocessed", event_json)
        r.rpush("queue:document.preprocessed", event_json)
    except Exception:
        # If Redis is offline in local dev / test mock mode, event is still returned
        pass

    return event_payload
