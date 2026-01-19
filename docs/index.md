# OpenAPI Contract Tester

This project performs **live contract testing** using an OpenAPI
specification as the source of truth.

The OpenAPI spec defines the contract.
The running API is tested against it.

If the API and spec diverge, tests fail.

## Quick Start

```bash
pip install pytest-openapi
pytest --openapi=http://localhost:8000
```

## Command-Line Options

### `--openapi=BASE_URL`
Run contract tests against the API at the specified base URL.

### `--openapi-no-strict-example-checking`
Use lenient validation for example-based tests. In this mode, responses are validated for structure and types only, without enforcing exact values or array lengths.

**When to use**:
- Examples contain placeholder or sample data
- Dynamic values vary per request (timestamps, IDs, durations)
- Array lengths differ from examples in real responses

See [Validation Modes](how-it-works/validation-modes.md) for details.

## Features

- ✅ Tests against live APIs
- ✅ Validates OpenAPI spec quality
- ✅ Generates test cases from schemas
- ✅ Hybrid validation (strict + lenient modes)
- ✅ Supports GET, POST, PUT, DELETE
- ✅ Readable test reports