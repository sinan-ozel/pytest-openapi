"""Pytest plugin for OpenAPI contract testing."""


def pytest_addoption(parser):
    """Add --openapi CLI option."""
    group = parser.getgroup("openapi")
    group.addoption(
        "--openapi",
        action="store",
        metavar="BASE_URL",
        help="Run OpenAPI contract tests against the specified base URL",
    )
    group.addoption(
        "--openapi-no-strict-example-checking",
        action="store_true",
        default=False,
        help="Use lenient schema validation for example responses instead of strict matching",
    )
    group.addoption(
        "--openapi-markdown-output",
        action="store",
        metavar="FILENAME",
        default=None,
        help="Write test results in Markdown format to the specified file",
    )
    group.addoption(
        "--openapi-no-stdout",
        action="store_true",
        default=False,
        help="Suppress all output to stdout",
    )


def pytest_configure(config):
    """Configure pytest with OpenAPI marker."""
    config.addinivalue_line(
        "markers",
        "openapi: OpenAPI contract tests",
    )

    # If --openapi flag is provided, validate and test the OpenAPI spec
    base_url = config.getoption("--openapi")
    strict_examples = not config.getoption(
        "--openapi-no-strict-example-checking"
    )
    markdown_output_file = config.getoption("--openapi-markdown-output")
    no_stdout = config.getoption("--openapi-no-stdout")

    if base_url:
        import pytest
        import requests

        from .contract import (
            get_test_report,
            test_delete_endpoint,
            test_get_endpoint,
            test_post_endpoint,
            test_put_endpoint,
        )
        from .openapi import validate_openapi_spec

        # Run validation checks
        validate_openapi_spec(base_url)

        # Fetch the OpenAPI spec
        try:
            response = requests.get(f"{base_url}/openapi.json", timeout=10)
            response.raise_for_status()
            spec = response.json()
        except Exception as e:
            pytest.exit(f"\n❌ Failed to fetch OpenAPI spec: {e}", returncode=1)

        # Reset server state if /reset endpoint exists (for testing)
        try:
            reset_response = requests.post(f"{base_url}/reset", timeout=5)
            if reset_response.status_code == 200:
                print(f"🔄 Server state reset via {base_url}/reset")
        except Exception:
            # Server doesn't have /reset endpoint or it failed - that's OK
            pass

        # Run contract tests on all endpoints
        # Execute tests grouped by HTTP method to avoid state pollution:
        # 1. GET (read initial state)
        # 2. POST (create new resources)
        # 3. PUT (update resources)
        # 4. DELETE (remove resources)
        paths = spec.get("paths", {})
        errors = []

        for method in ["get", "post", "put", "delete"]:
            for path, path_item in paths.items():
                if method not in path_item:
                    continue

                operation = path_item[method]

                # Select appropriate test function
                if method == "get":
                    success, error = test_get_endpoint(
                        base_url, path, operation, strict_examples
                    )
                elif method == "post":
                    success, error = test_post_endpoint(
                        base_url, path, operation, strict_examples
                    )
                elif method == "put":
                    success, error = test_put_endpoint(
                        base_url, path, operation, strict_examples
                    )
                elif method == "delete":
                    success, error = test_delete_endpoint(
                        base_url, path, operation, strict_examples
                    )

                if not success:
                    errors.append(f"  {method.upper()} {path}: {error}")

        # Generate and save/display report
        # Write markdown report to file if requested
        if markdown_output_file:
            from .contract import get_test_report_markdown
            try:
                with open(markdown_output_file, 'w', encoding='utf-8') as f:
                    f.write(get_test_report_markdown())
                if not no_stdout:
                    print(f"\n📝 Markdown report written to: {markdown_output_file}")
            except Exception as e:
                print(f"\n⚠️  Warning: Failed to write markdown report: {e}")

        # Display report to stdout unless suppressed
        if not no_stdout:
            print("\n")
            print(get_test_report())

        # Report results and exit
        if errors:
            if not no_stdout:
                print("\n❌ Contract tests failed:")
                for error in errors:
                    print(error)
            pytest.exit("Contract tests failed", returncode=1)
        else:
            if not no_stdout:
                print("\n✅ All contract tests passed!")
            # Don't call sys.exit(0) - let pytest finish normally


def pytest_unconfigure(config):
    """Clean up when pytest unconfigures.

    This hook is added to prevent conflicts with pytest-depends plugin.
    When pytest-openapi calls pytest.exit() during pytest_configure,
    it can interfere with pytest-depends' internal state management.
    This hook ensures proper cleanup happens.
    """
    # No specific cleanup needed for pytest-openapi,
    # but defining this hook prevents the IndexError in pytest-depends
    pass
