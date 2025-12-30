FROM python:3.11-slim

WORKDIR /app

# Copy pyproject.toml from the parent directory
COPY pyproject.toml .
COPY src/pytest_openapi ./pytest_openapi

# Copy only the test files (not the entire tests directory to avoid nested discovery)
COPY tests/__init__.py /test_of_tests/
COPY tests/test_*.py /test_of_tests/

RUN pip install --upgrade pip
RUN pip install .           # Install main project dependencies
RUN pip install .[test]     # Install test dependencies

# Copy sample tests after installation to avoid package discovery conflicts
COPY tests/test_samples /app/test_samples/

# Default command: run tests
CMD ["pytest", "/test_of_tests", "-v"]