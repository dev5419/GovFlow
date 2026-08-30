# ==============================================================================
# GovFlow AI Workers (Celery / PaddleOCR / LayoutLMv3) Dockerfile
# ==============================================================================
FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    gcc \
    libpq-dev \
    libgl1 \
    libglib2.0-0 \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

COPY apps/ai-workers/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy shared packages and worker application code
COPY packages/ ./packages/
COPY apps/ai-workers/ ./

CMD ["celery", "-A", "src.queue.tasks", "worker", "--loglevel=info"]