# Use a lightweight Python base image
FROM python:3.11-slim

# Set working directory
WORKDIR /workspace

# Install system dependencies (if needed)
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

