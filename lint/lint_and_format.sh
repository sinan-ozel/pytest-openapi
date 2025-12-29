#!/bin/bash

# Script to run all linting and reformatting steps from GitHub Actions locally
# This script mirrors the reformat and lint jobs from .github/workflows/ci.yaml

set -e  # Exit on error

echo "=========================================="
echo "Installing dependencies..."
echo "=========================================="
pip install --upgrade pip
pip install .[dev]

echo ""
echo "=========================================="
echo "Running Black (code formatter)..."
echo "=========================================="
black src/

echo ""
echo "=========================================="
echo "Running docformatter (docstring formatter)..."
echo "=========================================="
docformatter \
  --in-place \
  --recursive \
  --wrap-summaries 72 \
  --wrap-descriptions 72 \
  src/ || true

echo ""
echo "=========================================="
echo "Running isort (import sorter)..."
echo "=========================================="
isort src/

echo ""
echo "=========================================="
echo "Running Ruff (linter)..."
echo "=========================================="
ruff check ./src

echo ""
echo "=========================================="
echo "All linting and formatting steps completed!"
echo "=========================================="
