#!/usr/bin/env bash
set -euo pipefail

PYTEST_ARGS=(
  "--openapi=http://localhost:8000"
  "--openapi-no-strict-example-checking"
  "--openapi-markdown-output=report.md"
  "--openapi-no-stdout"
  "--openapi-timeout=60"
  "-v"
)

echo "Running pytest with OpenAPI options: ${PYTEST_ARGS[*]}"
pytest "${PYTEST_ARGS[@]}"
