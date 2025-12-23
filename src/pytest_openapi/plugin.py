"""Pytest plugin for OpenAPI contract testing."""

import pytest


def pytest_addoption(parser):
    """Add --openapi CLI option."""
    group = parser.getgroup("openapi")
    group.addoption(
        "--openapi",
        action="store",
        metavar="BASE_URL",
        help="Run OpenAPI contract tests against the specified base URL",
    )


def pytest_configure(config):
    """Configure pytest with OpenAPI marker."""
    config.addinivalue_line(
        "markers",
        "openapi: OpenAPI contract tests",
    )

    # If --openapi flag is provided, validate and test the OpenAPI spec
    base_url = config.getoption("--openapi")
    if base_url:
        import sys
        from .openapi import validate_openapi_spec
        from .contract import (
            test_get_endpoint,
            test_post_endpoint,
            test_put_endpoint,
            test_delete_endpoint,
            get_test_report,
        )
        import requests

        # Run validation checks
        validate_openapi_spec(base_url)

        # Fetch the OpenAPI spec
        try:
            response = requests.get(f"{base_url}/openapi.json", timeout=10)
            response.raise_for_status()
            spec = response.json()
        except Exception as e:
            print(f"\n❌ Failed to fetch OpenAPI spec: {e}")
            sys.exit(1)

        # Run contract tests on all endpoints
        paths = spec.get("paths", {})
        errors = []

        for path, path_item in paths.items():
            for method in ["get", "post", "put", "delete"]:
                if method not in path_item:
                    continue

                operation = path_item[method]

                # Select appropriate test function
                if method == "get":
                    success, error = test_get_endpoint(
                        base_url, path, operation
                    )
                elif method == "post":
                    success, error = test_post_endpoint(
                        base_url, path, operation
                    )
                elif method == "put":
                    success, error = test_put_endpoint(
                        base_url, path, operation
                    )
                elif method == "delete":
                    success, error = test_delete_endpoint(
                        base_url, path, operation
                    )

                if not success:
                    errors.append(f"  {method.upper()} {path}: {error}")

        # Generate and display human-readable report
        print("\n")
        print(get_test_report())

        # Report results and exit
        if errors:
            print(f"\n❌ Contract tests failed:")
            for error in errors:
                print(error)
            sys.exit(1)
        else:
            print(f"\n✅ All contract tests passed!")
            sys.exit(0)
