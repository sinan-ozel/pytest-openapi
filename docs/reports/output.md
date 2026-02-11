# Test Reports

pytest-openapi generates detailed test reports showing the results of all contract tests.

## Report Formats

### Console Output (Default)

By default, OpenAPI tests appear as individual pytest test items in the standard pytest output:

```
============================= test session starts ==============================
collected 3 items
created 4 items from openapi examples
created 20 items generated from schema

tests/test_samples/test_sample_math.py::test_sample_addition PASSED [  3%]
.::test_openapi[GET /users] PASSED [  7%]
.::test_openapi[POST /users [example-1]] PASSED [ 11%]
.::test_openapi[POST /users [generated-2]] PASSED [ 15%]
...

======================== 24 passed in 0.95s =========================
```

OpenAPI tests are dynamically injected during collection and appear with the `.::test_openapi[...]` prefix.

After pytest's standard collection, you'll see messages showing:
- How many test items were created from OpenAPI examples
- How many test items were generated from schemas

Each OpenAPI test case appears as a separate pytest item with descriptive test IDs:
- `.::test_openapi[GET /users]` - GET endpoint tests
- `.::test_openapi[POST /users [example-1]]` - Example-based POST test
- `.::test_openapi[POST /users [generated-2]]` - Schema-generated POST test

### Markdown Output (Default)

A detailed Markdown report is automatically written to a file. By default, the plugin will suggest a location or you can specify one:

```bash
pytest --openapi=http://localhost:8000 --openapi-markdown-output=report.md
```

The markdown report includes:
- Summary statistics with emoji indicators (✅/❌)
- Formatted code blocks for JSON data
- Clear sections for request/response
- Test case origin labels (📋 example / 🔧 schema-generated)
- Detailed error messages for failed tests

See the [example_report.md](../example_report.md) for a sample output.

### Verbose Contract Report

The detailed contract report with full request/response details is **not** printed to stdout by default (only written to the markdown file). This keeps the console output clean and focused on pytest's test results.

If you want to see the full contract report in the console, you can read the markdown file or implement custom reporting.

### Silent Mode

Suppress all stdout output using `--openapi-no-stdout`:

```bash
pytest --openapi=http://localhost:8000 --openapi-no-stdout
```

This is useful for:
- CI/CD pipelines where you only need the exit code
- Generating file output without console clutter
- Automated testing workflows

You can combine silent mode with markdown output:

```bash
pytest --openapi=http://localhost:8000 \
  --openapi-markdown-output=report.md \
  --openapi-no-stdout
```

### Verbose Output Options

#### Normal Mode (default)
In non-verbose mode, OpenAPI tests show as dots (`.`) or F for failures:

```
tests/test_samples/test_sample_math.py ..
[pytest-openapi] . F..........
```

The `[pytest-openapi]` label appears before the first OpenAPI test to distinguish them from regular pytest tests.

#### Verbose Mode (`-v`)
Shows each test with its full test ID:

```
.::test_openapi[GET /users] PASSED
.::test_openapi[POST /users [example-1]] PASSED
```

#### Very Verbose Mode (`-vv`)
Shows test details with truncated request/response (50 characters):

```
.::test_openapi[POST /users [example-1]] PASSED
  Request: {"name": "Alice", "email": "alice@example...
  Expected [201]: {"id": 1, "name": "Alice", "email": "alic...
  Actual [201]: {"id": 123, "name": "Alice", "email": "...
```

#### Very Very Verbose Mode (`-vvv`)
Shows full request/response without truncation:

```
.::test_openapi[POST /users [example-1]] PASSED
  Request: {
    "name": "Alice",
    "email": "alice@example.com"
  }
  Expected [201]: {
    "id": 1,
    "name": "Alice",
    "email": "alice@example.com"
  }
  Actual [201]: {
    "id": 123,
    "name": "Alice",
    "email": "alice@example.com"
  }
```

## Report Contents

Each test records:
- HTTP method and path
- Request body (if applicable)
- Expected status code and response body
- Actual status code and response body
- Pass/fail result with error details
- Test case origin (example-based or schema-generated)

A formatted report is generated at the end of execution showing all tests and a summary of results.