FROM python:3.11-slim

WORKDIR /app

# Copy pyproject.toml from the parent directory
COPY pyproject.toml .
COPY src/pytest_openapi ./pytest_openapi
COPY tests ./tests

RUN pip install --upgrade pip
RUN pip install .           # Install main project dependencies
RUN pip install .[test]     # Install test dependencies

# Default command: run tests
CMD ["pytest"]
