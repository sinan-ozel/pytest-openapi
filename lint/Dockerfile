FROM python:3.11-slim

WORKDIR /workspace

# Copy only pyproject.toml to install dependencies
COPY pyproject.toml /tmp/pyproject.toml
COPY src/pytest_openapi/__init__.py /tmp/src/pytest_openapi/__init__.py

RUN pip install --upgrade pip && \
    cd /tmp && \
    pip install . && \
    pip install .[dev] && \
    rm -rf /tmp/*

# Files will be mounted at /workspace
CMD ["./lint/lint_and_format.sh"]