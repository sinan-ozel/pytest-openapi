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

### `--openapi-markdown-output=FILENAME`
Write test results in Markdown format to the specified file.

**Usage**:
```bash
pytest --openapi=http://localhost:8000 --openapi-markdown-output=report.md
```

The markdown report includes:
- Summary statistics (total, passed, failed tests)
- Formatted code blocks for JSON data
- Clear sections for expected vs actual responses
- Error details in formatted blocks

The markdown report is written independently of stdout output.

### `--openapi-no-stdout`
Suppress all output to stdout. Useful for CI/CD pipelines where you only need the exit code or want to generate a file output without console output.

**Usage**:
```bash
pytest --openapi=http://localhost:8000 --openapi-no-stdout
```

This will:
- Suppress all output to stdout
- Still return appropriate exit codes (0 for success, 1 for failure)
- Can be combined with `--openapi-markdown-output` to only generate a file

**Combined usage**:
```bash
pytest --openapi=http://localhost:8000 \
  --openapi-markdown-output=report.md \
  --openapi-no-stdout
```

## Features

- ✅ Tests against live APIs
- ✅ Validates OpenAPI spec quality
- ✅ Generates test cases from schemas
- ✅ Hybrid validation (strict + lenient modes)
- ✅ Supports GET, POST, PUT, DELETE
- ✅ Readable test reports