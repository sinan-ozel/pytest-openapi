#!/usr/bin/env bash
set -euo pipefail

SERVICE="$1"

if [ -z "$SERVICE" ]; then
  echo "Usage: $0 <service-name>"
  exit 2
fi

# Strip "mock-server-" prefix and replace hyphens with underscores
SERVICE_DIR="${SERVICE#mock-server-}"
SERVICE_DIR="${SERVICE_DIR//-/_}"

# Get the directory of this script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

# Create a docker network for this test run
NETWORK_NAME="pytest-openapi-test-$$"
echo "🌐 Creating network: $NETWORK_NAME"
docker network create "$NETWORK_NAME" 2>/dev/null || true

# Cleanup function
cleanup() {
  echo ""
  echo "🧹 Cleaning up..."
  docker rm -f "mock-server-$$" 2>/dev/null || true
  docker network rm "$NETWORK_NAME" 2>/dev/null || true
}
trap cleanup EXIT

# Build the mock server image
echo "🔨 Building mock server image..."
docker build -t "pytest-openapi-${SERVICE}" -f "${PROJECT_ROOT}/tests/test_servers/${SERVICE_DIR}/Dockerfile" "${PROJECT_ROOT}/tests/test_servers/${SERVICE_DIR}"

# Start the mock server on the network
echo "🚀 Starting mock server: $SERVICE"
docker run -d \
  --name "mock-server-$$" \
  --network "$NETWORK_NAME" \
  --network-alias mock-server \
  "pytest-openapi-${SERVICE}"

# Wait for the mock server to be ready
echo "⏳ Waiting for mock server to be ready..."
READY=1
for i in $(seq 1 30); do
  # Check if Flask server has started by looking for "Running on" in logs
  if docker logs "mock-server-$$" 2>&1 | grep -q "Running on"; then
    READY=0
    echo "✅ Mock server is ready"
    break
  fi
  sleep 1
done

if [ "$READY" -ne 0 ]; then
  echo "❌ Service $SERVICE failed to become ready within 30s"
  exit 3
fi

# Build the test runner image
echo "🔨 Building test runner image..."
docker build -t pytest-openapi-test-runner -f "${PROJECT_ROOT}/.vscode/Dockerfile.test" "${PROJECT_ROOT}"

# Run pytest in a new container with source mounted
echo "🧪 Running pytest with --openapi=http://mock-server:8000"
echo "=================================================="
docker run --rm -it \
  --network "$NETWORK_NAME" \
  -v "${PROJECT_ROOT}/src:/workspace/src" \
  -v "${PROJECT_ROOT}/tests:/workspace/tests" \
  -e PYTHONPATH=/workspace/src \
  pytest-openapi-test-runner \
  pytest --openapi=http://mock-server:8000 --openapi-markdown-output=/workspace/tests/report.md /workspace/tests/test_openapi_generated.py /workspace/tests/test_samples/ -v

RC=$?
echo "=================================================="
exit $RC
