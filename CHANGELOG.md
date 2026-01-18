# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
