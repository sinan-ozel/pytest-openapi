# Test Servers

This directory contains mock servers used for integration testing of pytest-openapi.

## Structure

Each subdirectory represents a test scenario:

- `missing_openapi/` - Server without `/openapi.json` endpoint (tests error handling)

## Running Locally

Each server can be run independently for debugging:

```bash
cd test_servers/missing_openapi
docker build -t mock-server-missing-openapi .
docker run -p 8001:8000 mock-server-missing-openapi
```

## Adding New Test Servers

1. Create a new directory under `test_servers/`
2. Add `server.py`, `Dockerfile`, and `requirements.txt`
3. Register the service in `../docker-compose.yaml`
4. Add corresponding integration tests in `../test_integration.py`
