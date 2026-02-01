# Test Reports

pytest-openapi generates detailed test reports showing the results of all contract tests.

## Report Formats

### Console Output (Default)

By default, test results are printed to stdout with a human-readable format:

```
================================================================================
OpenAPI Contract Test Report
================================================================================

Test #1 ✅
📋 Test case from OpenAPI example
GET /users

Expected 200
  [
    {
      "id": 1,
      "name": "Alice",
      "email": "alice@example.com"
    }
  ]

Actual 200
  [
    {
      "id": 1,
      "name": "Alice",
      "email": "alice@example.com"
    }
  ]

--------------------------------------------------------------------------------
```

### Markdown Output

Generate a Markdown-formatted report using the `--openapi-markdown-output=FILENAME` flag:

```bash
pytest --openapi=http://localhost:8000 --openapi-markdown-output=report.md
```

The markdown report includes:
- Summary statistics with emoji indicators (✅/❌)
- Formatted code blocks for JSON data
- Clear sections for request/response
- Test case origin labels (📋 example / 🔧 schema-generated)

See the [example_report.md](../example_report.md) for a sample output.

### Silent Mode

Suppress stdout output using `--openapi-no-stdout`:

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