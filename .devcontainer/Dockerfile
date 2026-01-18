FROM python:3.11-bookworm

WORKDIR /workspace

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    ca-certificates \
    curl \
    git \
    jq \
    tree \
    apt-transport-https \
    wget \
    gnupg \
    lsb-release \
 && rm -rf /var/lib/apt/lists/*


COPY pyproject.toml .
COPY src/ ./src/
COPY tests/ ./tests/

RUN useradd -m vscode && \
    mkdir -p /home/vscode && \
    chown -R vscode:vscode /home/vscode

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install -e .[test]
RUN pip install -e .[dev]
RUN pip install -e .[docs]

SHELL ["/bin/bash", "-c"]

