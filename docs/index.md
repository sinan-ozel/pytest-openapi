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
By default, this is written to the file `report.md` in the current folder.

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

### Verbose Output Options

Control the level of detail in test output:

- **Default**: Shows dots (`.`) for passed tests, `F` for failures. OpenAPI tests are marked with `[pytest-openapi]` label.
- **`-v`**: Shows full test names for each test
- **`-vv`**: Shows request, expected response, and actual response (truncated to 50 characters)
- **`-vvv`**: Shows full request and response without truncation

Example:
```bash
pytest --openapi=http://localhost:8000 -vv
```

See [Output Formats](reports/output.md) for detailed examples.

### `--openapi-ignore=REGEXP`
Completely ignore endpoints whose path matches the provided regular expression. Use this to skip known-broken, auth-protected, or otherwise irrelevant endpoints during contract testing.

**Examples**:

```bash
pytest --openapi=http://localhost:8000 --openapi-ignore=mcp
pytest --openapi=http://localhost:8000 --openapi-ignore=(auth|mcp)
pytest --openapi=http://localhost:8000 --openapi-ignore=(v[0-9]+/auth|mcp)
```

This will:
- Suppress all output to stdout
- Still return appropriate exit codes (0 for success, 1 for failure)
- Can be combined with `--openapi-markdown-output=FILENAME` to only generate a file

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