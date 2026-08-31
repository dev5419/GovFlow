import asyncio
import json
import logging
from redis.asyncio import Redis
from src.config.settings import settings
from src.events.subscribers.report_generated import handle_report_generated_event
from src.events.subscribers.extraction_completed import handle_extraction_completed_event

logger = logging.getLogger(__name__)

async def start_redis_subscribers():
    """
    Background task to listen to Redis pub/sub channels.
    """
    redis = Redis.from_url(settings.redis_url)
    pubsub = redis.pubsub()
    
    await pubsub.subscribe("report.generated")
    await pubsub.subscribe("document.extraction.completed")
    
    logger.info("Started listening to Redis channels: report.generated, document.extraction.completed")
    
    try:
        async for message in pubsub.listen():
            if message["type"] == "message":
                channel = message["channel"].decode("utf-8")
                
                if channel == "report.generated":
                    await handle_report_generated_event(message)
                elif channel == "document.extraction.completed":
                    # Extraction completed logic was implemented in Module 3.2
                    await handle_extraction_completed_event(message)
    except asyncio.CancelledError:
        logger.info("Redis subscriber task cancelled.")
    finally:
        await pubsub.unsubscribe()
        await redis.close()
