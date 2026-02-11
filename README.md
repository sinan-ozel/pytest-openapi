![Tests & Lint](https://github.com/sinan-ozel/pytest-openapi/actions/workflows/ci.yaml/badge.svg?branch=main)
![PyPI](https://img.shields.io/pypi/v/pytest-openapi.svg)
![Downloads](https://static.pepy.tech/badge/pytest-openapi)
![Monthly Downloads](https://static.pepy.tech/badge/pytest-openapi/month)
[![Documentation](https://img.shields.io/badge/docs-mkdocs-blue)](https://sinan-ozel.github.io/pytest-openapi/)
![License](https://img.shields.io/github/license/sinan-ozel/pytest-openapi.svg)
![Python](https://img.shields.io/badge/Python-3.11%2B-blue)
![Made with Love](https://img.shields.io/badge/Made%20with-❤️-red)

# 🧪 OpenAPI Contract Tester

An opinionated, lightweight **black-box contract tester** against a **live API** using its OpenAPI specification as the source of truth.

This tool validates OpenAPI quality, generates test cases from schemas, and verifies that real HTTP responses match the contract.
This "certifies" that the documentation is complete with descriptions, example, and schema, and that the endpoint behaves as the documentation suggests.

## Guiding Principles:
1. A service needs to document clearly. (This means schemas, descriptions, and examples)
2. When the examples and schemas are used, it should respond as expected from the documentation.

📚 **[Read the full documentation](https://sinan-ozel.github.io/pytest-openapi/)**

## ✨ What it does

### ▶️ Quick Example

![Swagger POST endpoint /email](swagger-screenshot-1.png)

```bash
pytest --openapi=http://localhost:8000
```

**Console Output:**
```
============================= test session starts ==============================
collected 27 items

tests/test_openapi_generated.py::test_openapi_endpoint[GET /users] PASSED [  3%]
tests/test_openapi_generated.py::test_openapi_endpoint[POST /email [example-1]] PASSED [  7%]
tests/test_openapi_generated.py::test_openapi_endpoint[POST /email [generated-2]] PASSED [ 11%]
...

📝 Full test report saved to: tests/report.md
   (Configure output file with: --openapi-markdown-output=<filename>)

======================== 27 passed in 0.95s =========================
```

**Detailed Report** (`report.md`):
```
Test #10 ✅
POST /email
Requested:
  {
    "body": "Lorem ipsum dolor sit amet",
    "from": "Lorem ipsum dolor sit amet",
    "subject": "Lorem ipsum dolor sit amet",
    "to": "Test!@#$%^&*()_+-=[]{}|;:<>?,./`~"
  }

Expected 201
  {
    "body": "Hi Bob, how are you?",
    "from": "alice@example.com",
    "id": 1,
    "subject": "Hello",
    "to": "bob@example.com"
  }

Actual 201
  {
    "body": "Lorem ipsum dolor sit amet",
    "from": "Lorem ipsum dolor sit amet",
    "id": 10,
    "subject": "Lorem ipsum dolor sit amet",
    "to": "Test!@#$%^&*()_+-=[]{}|;:<>?,./`~"
  }

```

Each OpenAPI test appears as an individual pytest test item.

✔️ Validates OpenAPI request/response definitions
✔️ Enforces schema field descriptions
✔️ Generates test cases from schemas, checks response codes and types in the response
✔️ Tests the exanples
✔️ Tests **GET / POST / PUT / DELETE** endpoints
✔️ Compares live responses against examples
✔️ Produces a readable test report


# ▶️ Detailed Example

## Install
```bash
pip install pytest-openapi
```

## Run

Say that you have a service running at port `8000` on `localhost`. Then, run:

```bash
pytest --openapi=http://localhost:8000
```

### Options

- `--openapi=BASE_URL`: Run contract tests against the API at the specified base URL
- `--openapi-no-strict-example-checking`: Use lenient validation for example-based tests
- `--openapi-markdown-output=FILENAME`: Write test results in Markdown format to the specified file
- `--openapi-no-stdout`: Suppress all output to stdout
- `--openapi-ignore=REGEXP`: Completely ignore endpoints whose path matches the given regular expression. Useful to skip known-broken or auth-protected paths.

Examples:

```bash
pytest --openapi=http://localhost:8000 --openapi-ignore=mcp
pytest --openapi=http://localhost:8000 --openapi-ignore=(auth|mcp)
pytest --openapi=http://localhost:8000 --openapi-ignore=(v[0-9]+/auth|mcp)
```

#### Strict vs Lenient Example Checking

By default, pytest-openapi performs **strict matching** on example-based tests:
- When your OpenAPI spec includes explicit request/response examples, the actual response must match the example values exactly
- This ensures examples accurately reflect real API behavior

However, sometimes examples contain placeholder values (like `[1, 2, 3]`) that don't match actual responses (like `[]`). Use `--openapi-no-strict-example-checking` for lenient validation:

```bash
pytest --openapi=http://localhost:8000 --openapi-no-strict-example-checking
```

**Lenient mode** validates:
- Structure and types match (all expected keys present, correct types)
- But ignores exact values and array lengths

**Note**: Schema-generated tests always use schema validation (not affected by this flag).

#### Markdown Output Format

You can generate test reports in Markdown format and save them to a file:

```bash
pytest --openapi=http://localhost:8000 --openapi-markdown-output=report.md
```

This creates a `report.md` file with:
- Summary statistics (total, passed, failed tests)
- Formatted code blocks for JSON data
- Clear sections for expected vs actual responses
- Error details in formatted blocks

The markdown report is written independently of stdout output.

**Example output**: See [example_report.md](example_report.md) for a sample markdown report.

#### Suppress Stdout

For CI/CD pipelines where you want completely silent operation or only care about the exit code:

```bash
pytest --openapi=http://localhost:8000 --openapi-no-stdout
```

This will:
- Suppress all output to stdout
- Still return appropriate exit codes (0 for success, 1 for failure)
- Can be combined with `--openapi-markdown-output` to only generate a file

You can combine flags for silent operation with file output:
```bash
pytest --openapi=http://localhost:8000 --openapi-markdown-output=report.md --openapi-no-stdout
```

## Server
See here an example server - `email-server`: [tests/test_servers/email_server/server.py](tests/test_servers/email_server/server.py)

## Resulting Tests

[tests/test_servers/email_server/email_test_output.txt](tests/test_servers/email_server/email_test_output.txt)

# Future Plans / TODO

This is a work in progress.
- [ ] A check that the example matches the schema
- [ ] Ask that 400 responses be in the documentation.
- [ ] A check for regexp and email formats.

## Issues? Feedback?

Seriously, this is a work-in-progress. If you try it and something does not work as intended, or expect, open a ticket!
I may be able to fix quickly, especially if you can provide a minimal example to replicate the issue.

## In Consideration
- [ ] Use LLM-as-a-judge to assess the error messages and check their spelling.

# Contributing
Contributions are welcome!

The only requirement is 🐳 Docker.

Test are containerized, run them using the VS Code task `test`. If you don't want to use VS Code, the command is `docker compose -f ./tests/docker-compose.yaml --project-directory ./tests up --build --abort-on-container-exit --exit-code-from test`. Run this before making a PR, please.

There is also a development environment for VS Code, if you need it. On this environment, you can run the task `run-mock-server` to run one of the [mock servers](tests/test_servers) and see the output.

You can add your own mock server, and then add integration tests. Just follow the same pattern as every test to make a call - `subprocess.run('pytest', '--openapi=http://your-server:8000`.

Please reformat and lint before making a PR. The VS Task is `lint`, and if you don't want to use VS Code, the command is: `docker compose -f ./lint/docker-compose.yaml --project-directory ./lint up --build --abort-on-container-exit --exit-code-from linter`. Run this before making a PR, please.

If you add a functionality, please add to the the documentation.

Please submit a pull request or open an issue for any bugs or feature requests.

The moment your PR is merged, you get a dev release. You can then set up the version number to use your changes.

# License
MIT License. See [LICENSE](LICENSE) file for the specific wording.

