# Test Reports

pytest-openapi generates detailed test reports showing the results of all contract tests.

## Report Formats

### Console Output (Default)

By default, OpenAPI tests appear as individual pytest test items in the standard pytest output:

```
============================= test session starts ==============================
collected 27 items

tests/test_openapi_generated.py::test_openapi_endpoint[GET /users] PASSED [  3%]
tests/test_openapi_generated.py::test_openapi_endpoint[POST /users [example-1]] PASSED [  7%]
tests/test_openapi_generated.py::test_openapi_endpoint[POST /users [generated-2]] PASSED [ 11%]
...

======================== 27 passed in 0.95s =========================
```

Each OpenAPI test case appears as a separate pytest item with descriptive test IDs:
- `[GET /users]` - GET endpoint tests
- `[POST /users [example-1]]` - Example-based POST test
- `[POST /users [generated-2]]` - Schema-generated POST test

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

## Report Contents

Each test records:
- HTTP method and path
- Request body (if applicable)
- Expected status code and response body
- Actual status code and response body
- Pass/fail result with error details
- Test case origin (example-based or schema-generated)

A formatted report is generated at the end of execution showing all tests and a summary of results.