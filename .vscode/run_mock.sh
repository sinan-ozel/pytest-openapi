#!/usr/bin/env bash
set -euo pipefail

SERVICE="$1"

if [ -z "$SERVICE" ]; then
  echo "Usage: $0 <service-name>"
  exit 2
fi

# Start service detached
docker compose -f tests/docker-compose.yaml --project-directory tests up -d "$SERVICE"

# Wait up to 30s for the service to respond on /openapi.json
READY=1
for i in $(seq 1 30); do
  # Try probing the host-mapped port first (safer when curl isn't in the image)
  HOST_PORT=$(docker compose -f tests/docker-compose.yaml --project-directory tests port "$SERVICE" 8000 2>/dev/null | sed -n 's/.*://p' || true)
  if [ -n "$HOST_PORT" ]; then
    if curl -fsS "http://localhost:${HOST_PORT}/openapi.json" >/dev/null 2>&1; then
      READY=0
      break
    fi
  else
    # Fallback: try to curl from inside the container
    if docker compose -f tests/docker-compose.yaml --project-directory tests exec -T "$SERVICE" sh -c 'curl -fsS http://localhost:8000/openapi.json >/dev/null' 2>/dev/null; then
      READY=0
      break
    fi
  fi
  sleep 1
done

if [ "$READY" -ne 0 ]; then
  echo "❌ Service $SERVICE failed to become ready within 30s"
  docker compose -f tests/docker-compose.yaml --project-directory tests rm -fs "$SERVICE" || true
  exit 3
fi

# Run pytest in the test container against the service
docker compose -f tests/docker-compose.yaml --project-directory tests run --rm test pytest --openapi=http://"$SERVICE":8000 /app/test_samples/ -q
RC=$?

# Clean up the service container
docker compose -f tests/docker-compose.yaml --project-directory tests rm -fs "$SERVICE" || true

exit $RC
