#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
IMAGE_NAME="${IMAGE_NAME:-hello-world-api-v10}"
IMAGE_TAG="${IMAGE_TAG:-v10}"
CONTAINER_NAME="${CONTAINER_NAME:-hello-world-api-v10}"
HOST_PORT="${HOST_PORT:-8081}"
CONTAINER_PORT="${CONTAINER_PORT:-8081}"

IMAGE="${IMAGE_NAME}:${IMAGE_TAG}"

cd "$SCRIPT_DIR"

echo "Building ${IMAGE}..."
docker build --tag "$IMAGE" .

echo "Replacing container ${CONTAINER_NAME}..."
docker rm --force "$CONTAINER_NAME" >/dev/null 2>&1 || true
docker run --detach \
  --name "$CONTAINER_NAME" \
  --publish "${HOST_PORT}:${CONTAINER_PORT}" \
  "$IMAGE" >/dev/null

cleanup() {
  if ! docker ps --format '{{.Names}}' | grep -Fxq "$CONTAINER_NAME"; then
    echo "Container stopped unexpectedly. Logs:"
    docker logs "$CONTAINER_NAME" || true
    exit 1
  fi
}
trap cleanup EXIT

echo "Waiting for health endpoint..."
for attempt in {1..30}; do
  if curl --fail --silent "http://localhost:${HOST_PORT}/health" >/dev/null; then
    trap - EXIT
    echo "${IMAGE} is running at http://localhost:${HOST_PORT}"
    echo "Health:"
    curl --fail --silent "http://localhost:${HOST_PORT}/health"
    printf '\n'
    exit 0
  fi
  sleep 1
done

echo "Health check timed out. Logs:"
docker logs "$CONTAINER_NAME" || true
exit 1
