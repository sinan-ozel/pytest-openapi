import pytest

from pytest_openapi import contract


def test_openapi_endpoint(openapi_test_case, request):
    """Single test that runs the appropriate contract check for each endpoint.

    The `openapi_test_case` fixture is parametrized by `pytest_generate_tests`
    in the plugin and contains dict with: method, path, operation, request_body, test_origin.
    """
    method = openapi_test_case["method"]
    path = openapi_test_case["path"]
    operation = openapi_test_case["operation"]
    request_body = openapi_test_case["request_body"]
    test_origin = openapi_test_case["test_origin"]

    base_url = getattr(request.config, "_openapi_base_url", None)
    strict_examples = getattr(request.config, "_openapi_strict_examples", True)
    timeout = getattr(request.config, "_openapi_timeout", 10)

    func_map = {
        "get": contract.test_get_endpoint,
        "post": contract.test_post_endpoint_single,
        "put": contract.test_put_endpoint_single,
        "delete": contract.test_delete_endpoint,
    }

    test_fn = func_map.get(method)
    if test_fn is None:
        pytest.skip(f"Unsupported method: {method}")

    # For POST/PUT with specific request body, call the single test variant
    if method in ["post", "put"]:
        success, error = test_fn(
            base_url, path, operation, request_body, test_origin,
            strict_examples, timeout=timeout
        )
    else:
        # For GET/DELETE, use the original functions
        success, error = test_fn(
            base_url, path, operation, strict_examples, timeout=timeout
        )

    if not success:
        pytest.fail(f"{method.upper()} {path}: {error}")

