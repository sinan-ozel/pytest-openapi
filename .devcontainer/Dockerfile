FROM python:3.11-slim

WORKDIR /workspace

# Install system dependencies
RUN apt-get update && \
    apt-get install -y build-essential git vim && \
    rm -rf /var/lib/apt/lists/*

COPY pyproject.toml .
COPY src/ ./src/
COPY tests/ ./tests/

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install -e .[test]
RUN pip install -e .[dev]
RUN pip install -e .[docs]
