# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.4] - 2026-01-30

### Added
- `--openapi-markdown-output=FILENAME` flag to write a Markdown test report to a file and a Markdown report generator producing fenced JSON blocks, summary statistics, and test case origin tracking
- `--openapi-no-stdout` flag to suppress all report output to stdout (useful for CI)
- `--openapi-ignore=REGEXP` flag to completely ignore endpoints matching the provided regular expression (useful to skip known-broken or auth-protected paths)
- Enum validation support: generate invalid enum values for negative tests and detect invalid enum values in requests; includes a mock enum validation test server and integration tests
- Integration tests for output formats and new test servers (`tests/test_output_formats.py`, `tests/test_servers/enum_validation_test`)
- Documentation and example Markdown report; `docs-validate` Docker files and CI/docs updates

### Changed
- Reports now indicate test case origin (`example` vs `generated`) and include the Markdown report alongside the existing plain-text report
- Improved lenient-mode handling for documented 404 responses

### Fixed
- Fix nullable field validation for OpenAPI 3.0 and 3.1
- Fix 404 handling in lenient mode

## [0.1.3] - 2026-01-23

### Added
- New `--openapi-markdown-output=FILENAME` flag to generate test reports in Markdown format
- New `--openapi-no-stdout` flag to suppress all output to stdout (useful for CI/CD)
- Markdown report generator with formatted code blocks, summary statistics, and test case origin tracking
- Server state reset functionality (POST /reset endpoint) to ensure test isolation
- Documentation for markdown output and stdout suppression features

### Changed
- Tests now execute in method-grouped order (GET → POST → PUT → DELETE) to avoid state pollution
- PUT endpoints now only use example-based tests (skip schema-generated tests) to avoid issues with path parameters that reference specific resource IDs
- Server state is reset at test start if /reset endpoint is available
- `pytest_unconfigure` hook added to prevent conflicts with pytest-depends plugin

### Fixed
- PUT endpoint testing improved by removing schema-generated tests that don't work well with path parameters
- IndexError in pytest-depends plugin interaction resolved by adding cleanup hook

### Removed
- Removed completed TODO items from README (description requirement toggle, 400 message checks)

## [0.1.2] - 2026-01-18

### Added
- New `--openapi-no-strict-example-checking` flag for lenient example validation
- Schema-based validation function `validate_against_schema()` for proper JSON Schema checking
- Hybrid validation approach: strict matching for examples, schema validation for generated tests
- Test tracking to distinguish between example-based and schema-generated test cases
- Lenient comparison mode that validates structure and types without enforcing exact values

### Changed
- Example-based tests now support both strict (default) and lenient validation modes
- Schema-generated tests now use proper JSON Schema validation instead of example comparison
- Improved array validation to check element types without enforcing exact lengths in lenient mode

### Fixed
- Example values no longer incorrectly fail when structure matches but values differ (with lenient mode)
- Array length mismatches in examples now properly handled in lenient mode

## [0.1.1] - 2026-01-18

### Added
- Support for accepting 501 (Not Implemented) status codes when documented in OpenAPI spec
- Test coverage for 501 responses (both documented and undocumented scenarios)

### Fixed
- Fixed missing return statement in `make_request()` function that caused NoneType errors
- Contract tests now properly accept documented 501 responses as valid

### Changed
- Contract validation now only accepts success codes (200/201/204) and documented 501 responses
- Other documented error codes (400, 404, 422, etc.) are still treated as test failures

## [0.1.0] - 2025-12-23

### Added
- Initial release of pytest-openapi
- Automatic contract testing against OpenAPI specifications
- Support for GET, POST, PUT, and DELETE endpoints
- Schema-based test case generation
- Nested object and array validation
- Example-based testing
- Command-line interface via `--openapi` flag
- Comprehensive error reporting with detailed diff output
