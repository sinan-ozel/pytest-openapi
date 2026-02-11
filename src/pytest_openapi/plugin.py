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
    group.addoption(
        "--openapi-timeout",
        action="store",
        metavar="SECONDS",
        default=10,
        help="Timeout in seconds for HTTP requests to the target API",
    )
    group.addoption(
        "--openapi-ignore",
        action="store",
        metavar="REGEXP",
        default=None,
        help="Regular expression; endpoints with paths matching this will be ignored",
    )


def pytest_configure(config):
    """Configure pytest with OpenAPI marker and validate spec."""
    config.addinivalue_line(
        "markers",
        "openapi: OpenAPI contract tests",
    )

    # If --openapi flag is provided, validate and store the OpenAPI spec
    base_url = config.getoption("--openapi")

    if base_url:
        import re

        import pytest
        import requests

        from .openapi import validate_openapi_spec

        strict_examples = not config.getoption(
            "--openapi-no-strict-example-checking"
        )
        markdown_output_file = config.getoption("--openapi-markdown-output")
        no_stdout = config.getoption("--openapi-no-stdout")
        ignore_pattern = config.getoption("--openapi-ignore")
        openapi_timeout = float(config.getoption("--openapi-timeout"))

        # Run validation checks
        validate_openapi_spec(base_url, timeout=openapi_timeout)

        # Fetch the OpenAPI spec
        try:
            response = requests.get(
                f"{base_url}/openapi.json", timeout=openapi_timeout
            )
            response.raise_for_status()
            spec = response.json()
        except Exception as e:
            pytest.exit(f"\n❌ Failed to fetch OpenAPI spec: {e}", returncode=1)

        # Reset server state if /reset endpoint exists (for testing)
        try:
            reset_response = requests.post(
                f"{base_url}/reset", timeout=openapi_timeout
            )
            if reset_response.status_code == 200:
                if not no_stdout:
                    print(f"🔄 Server state reset via {base_url}/reset")
        except Exception:
            # Server doesn't have /reset endpoint or it failed - that's OK
            pass

        # Compile ignore pattern if provided
        ignore_re = None
        if ignore_pattern:
            try:
                ignore_re = re.compile(ignore_pattern)
            except Exception:
                pytest.exit(
                    f"Invalid regular expression for --openapi-ignore: {ignore_pattern}",
                    returncode=2,
                )

        # Store configuration on the config object for use during test generation and execution
        config._openapi_base_url = base_url
        config._openapi_spec = spec
        config._openapi_strict_examples = strict_examples
        config._openapi_timeout = openapi_timeout
        config._openapi_markdown_output = markdown_output_file
        config._openapi_no_stdout = no_stdout
        config._openapi_ignore_re = ignore_re
        config._openapi_ignore_pattern = ignore_pattern

        if not no_stdout:
            print(
                f"\n✅ OpenAPI spec validated and loaded from {base_url}/openapi.json"
            )

        if not no_stdout:
            print(
                f"\n✅ OpenAPI spec validated and loaded from {base_url}/openapi.json"
            )


def pytest_report_teststatus(report, config):
    """Customize test status reporting to show [pytest-openapi]
    label."""
    if report.when == "call" and hasattr(report, "nodeid"):
        if report.nodeid.startswith(".::test_openapi["):
            # First OpenAPI test - print label
            if not hasattr(config, "_openapi_label_printed"):
                config._openapi_label_printed = True
                # Return custom status that includes the label
                # Format: (category, letter, word)
                if report.outcome == "passed":
                    return "passed", "[pytest-openapi] .", "PASSED"
                elif report.outcome == "failed":
                    return "failed", "[pytest-openapi] F", "FAILED"
                elif report.outcome == "skipped":
                    return "skipped", "[pytest-openapi] s", "SKIPPED"
    return None


def pytest_collection_modifyitems(session, config, items):
    """Inject OpenAPI test items dynamically into the test collection.

    This hook allows us to add OpenAPI tests without requiring a test
    file.
    """
    # Check if --openapi flag was provided
    base_url = config.getoption("--openapi", default=None)
    if not base_url:
        return

    # Get stored configuration
    spec = getattr(config, "_openapi_spec", None)
    if not spec:
        return

    import pytest
    from _pytest.python import Module

    from . import contract
    from .case_generator import generate_test_cases_for_schema

    ignore_re = getattr(config, "_openapi_ignore_re", None)
    ignore_pattern = getattr(config, "_openapi_ignore_pattern", None)
    no_stdout = getattr(config, "_openapi_no_stdout", False)
    strict_examples = getattr(config, "_openapi_strict_examples", True)
    timeout = getattr(config, "_openapi_timeout", 10)

    # Create a virtual module to be parent of all OpenAPI test items
    # Use the session as parent
    module = Module.from_parent(session, path=session.path)
    module._openapi_virtual_module = True

    # Collect all test cases from the OpenAPI spec
    test_items = []
    paths = spec.get("paths", {})

    # Execute tests in order: GET -> POST -> PUT -> DELETE
    for method in ["get", "post", "put", "delete"]:
        for path, path_item in paths.items():
            if method not in path_item:
                continue

            # Check if path should be ignored
            if ignore_re and ignore_re.search(path):
                if not no_stdout:
                    print(
                        f"🔕 Ignoring {method.upper()} {path} due to --openapi-ignore={ignore_pattern}"
                    )
                continue

            operation = path_item[method]

            # For GET and DELETE: typically no request body, one test per endpoint
            if method in ["get", "delete"]:
                test_id = f"test_openapi[{method.upper()} {path}]"

                # Create test function for this endpoint
                def make_test_func(m, p, op):
                    def test_func():
                        func_map = {
                            "get": contract.test_get_endpoint,
                            "delete": contract.test_delete_endpoint,
                        }
                        test_fn = func_map[m]
                        success, error = test_fn(
                            base_url, p, op, strict_examples, timeout=timeout
                        )
                        if not success:
                            pytest.fail(f"{m.upper()} {p}: {error}")

                    return test_func

                test_func = make_test_func(method, path, operation)
                test_func.__name__ = test_id

                # Create pytest Function item
                item = pytest.Function.from_parent(
                    module,
                    name=test_id,
                    callobj=test_func,
                )
                item.add_marker(pytest.mark.openapi)
                test_items.append(item)

            # For POST and PUT: generate test cases from examples and schemas
            elif method in ["post", "put"]:
                request_body_def = operation.get("requestBody", {})
                request_content = request_body_def.get("content", {})

                request_test_cases = []
                test_origins = []

                for media_type, media_obj in request_content.items():
                    # Collect explicit examples
                    if "example" in media_obj:
                        request_test_cases.append(media_obj["example"])
                        test_origins.append("example")
                    if "examples" in media_obj:
                        examples_dict = media_obj["examples"]
                        for ex_name, ex_obj in examples_dict.items():
                            if "value" in ex_obj:
                                request_test_cases.append(ex_obj["value"])
                                test_origins.append("example")

                    # Generate test cases from schema
                    if "schema" in media_obj:
                        schema = media_obj["schema"]
                        generated, _ = generate_test_cases_for_schema(
                            schema, "request_body"
                        )
                        for gen_case in generated:
                            request_test_cases.append(gen_case)
                            test_origins.append("generated")
                    break

                # Create a test item for each request body variant
                for i, (req_body, origin) in enumerate(
                    zip(request_test_cases, test_origins)
                ):
                    origin_marker = (
                        "example" if origin == "example" else "generated"
                    )
                    test_id = f"test_openapi[{method.upper()} {path} [{origin_marker}-{i+1}]]"

                    # Create test function for this specific request
                    def make_test_func(m, p, op, rb, to):
                        def test_func():
                            func_map = {
                                "post": contract.test_post_endpoint_single,
                                "put": contract.test_put_endpoint_single,
                            }
                            test_fn = func_map[m]
                            success, error = test_fn(
                                base_url,
                                p,
                                op,
                                rb,
                                to,
                                strict_examples,
                                timeout=timeout,
                            )
                            if not success:
                                pytest.fail(f"{m.upper()} {p}: {error}")

                        return test_func

                    test_func = make_test_func(
                        method, path, operation, req_body, origin
                    )
                    test_func.__name__ = test_id

                    # Create pytest Function item
                    item = pytest.Function.from_parent(
                        module,
                        name=test_id,
                        callobj=test_func,
                    )
                    item.add_marker(pytest.mark.openapi)
                    test_items.append(item)

    # Add all OpenAPI test items to the collection
    items.extend(test_items)

    # Store the count for reporting after collection
    config._openapi_test_count = len(test_items)


def pytest_collection_finish(session):
    """Print message about OpenAPI tests after collection."""
    config = session.config

    # Only print if we added OpenAPI tests
    if hasattr(config, "_openapi_test_count"):
        count = config._openapi_test_count
        no_stdout = getattr(config, "_openapi_no_stdout", False)

        if count > 0 and not no_stdout:
            item_word = "item" if count == 1 else "items"
            print(f"created {count} {item_word} based on openapi schema")


def pytest_unconfigure(config):
    """Clean up when pytest unconfigures.

    This hook is added to prevent conflicts with pytest-depends plugin.
    When pytest-openapi calls pytest.exit() during pytest_configure, it
    can interfere with pytest-depends' internal state management. This
    hook ensures proper cleanup happens.
    """
    # No specific cleanup needed for pytest-openapi,
    # but defining this hook prevents the IndexError in pytest-depends
    pass


def pytest_sessionfinish(session, exitstatus):
    """Generate and save reports after all tests complete."""
    config = session.config

    # Only generate reports if --openapi was used
    if not hasattr(config, "_openapi_base_url"):
        return

    markdown_output_file = getattr(config, "_openapi_markdown_output", None)
    no_stdout = getattr(config, "_openapi_no_stdout", False)

    from .contract import get_test_report_markdown

    # Write markdown report to file if requested
    if markdown_output_file:
        try:
            with open(markdown_output_file, "w", encoding="utf-8") as f:
                f.write(get_test_report_markdown())
            if not no_stdout:
                print(f"\n📝 Full test report saved to: {markdown_output_file}")
                print(
                    "   (Configure output file with: --openapi-markdown-output=<filename>)"
                )
        except Exception as e:
            print(f"\n⚠️  Warning: Failed to write markdown report: {e}")

    # Don't display the full report to stdout anymore since tests appear as individual pytest items
    # Users can see test results in pytest's normal output
