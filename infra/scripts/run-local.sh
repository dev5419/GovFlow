#!/usr/bin/env bash
# ==============================================================================
# GovFlow — Start Local Development Stack via Docker Compose
# ==============================================================================
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "${SCRIPT_DIR}/../.." && pwd)"
COMPOSE_FILE="${ROOT_DIR}/infra/docker/docker-compose.yml"

echo "========================================================"
echo " Starting GovFlow Local Development Environment"
echo "========================================================"

# Copy .env.example if .env does not exist
if [ ! -f "${ROOT_DIR}/.env" ]; then
    echo "Creating .env from .env.example..."
    cp "${ROOT_DIR}/.env.example" "${ROOT_DIR}/.env"
fi

cd "${ROOT_DIR}"

echo "Checking Docker..."
if ! command -v docker >/dev/null 2>&1; then
    echo "Error: docker command not found. Please install Docker." >&2
    exit 1
fi

echo "Building and starting all containers..."
docker compose -f "${COMPOSE_FILE}" --env-file "${ROOT_DIR}/.env" up --build -d

echo ""
echo "========================================================"
echo " GovFlow Services Status:"
echo " - Next.js Web:       http://localhost:3000"
echo " - API Gateway:       http://localhost:8000"
echo " - API Docs (Swagger):http://localhost:8000/docs"
echo " - MinIO Console:     http://localhost:9001"
echo " - PostgreSQL 15:     localhost:5432"
echo " - Redis 7:           localhost:6379"
echo "========================================================"
echo "Use 'docker compose -f infra/docker/docker-compose.yml logs -f' to view logs."