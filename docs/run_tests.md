# Running the test suite with OpenAPI options

Use the following example command to run the test suite against a running mock server.

```bash
pytest --openapi=http://localhost:8000 \
  --openapi-no-strict-example-checking \
  --openapi-markdown-output=report.md \
  --openapi-no-stdout \
  --openapi-timeout=60 \
  -v
```

- `--openapi`: OpenAPI base URL to test against.
- `--openapi-no-strict-example-checking`: relaxes strict example validation.
- `--openapi-markdown-output=FILENAME`: path for a markdown report.
- `--openapi-no-stdout`: disable plugin stdout output (useful in CI).
- `--openapi-timeout`: request timeout in seconds.

You can also use the included helper script in `scripts/` to run the same command.

See other documentation pages for configuration and advanced usage.
