"""OpenAPI specification validation and parsing."""

import sys
import requests


def check_request_body_has_example(method, path, operation):
    """
    Check if a POST/PUT/DELETE operation has a request body example.

    Args:
        method: HTTP method (post, put, delete)
        path: API endpoint path
        operation: OpenAPI operation object

    Returns:
        str or None: Error message if example is missing, None otherwise
    """
    request_body = operation.get("requestBody", {})
    content = request_body.get("content", {})

    has_example = False
    for media_type, media_obj in content.items():
        if "example" in media_obj or "examples" in media_obj:
            has_example = True
            break

    if content and not has_example:
        return f"  - {method.upper()} {path}: Missing request body example"

    return None


def check_operation_has_responses(method, path, operation):
    """
    Check if an operation has response definitions.

    Args:
        method: HTTP method (get, post, put, delete)
        path: API endpoint path
        operation: OpenAPI operation object

    Returns:
        str or None: Error message if responses are missing, None otherwise
    """
    responses = operation.get("responses", {})
    if not responses:
        return f"  - {method.upper()} {path}: Missing response definitions"

    return None


def check_response_has_example(method, path, status_code, response_obj):
    """
    Check if a response definition has an example.

    Args:
        method: HTTP method (get, post, put, delete)
        path: API endpoint path
        status_code: HTTP status code
        response_obj: OpenAPI response object

    Returns:
        str or None: Error message if example is missing, None otherwise
    """
    content = response_obj.get("content", {})

    has_example = False
    for media_type, media_obj in content.items():
        if "example" in media_obj or "examples" in media_obj:
            has_example = True
            break

    if content and not has_example:
        return f"  - {method.upper()} {path}: Missing response example for status {status_code}"

    return None


def validate_openapi_spec(base_url):
    """
    Validate that the OpenAPI spec is available and meets requirements.

    Checks:
    1. /openapi.json endpoint is accessible
    2. All GET/POST/PUT/DELETE endpoints have request examples (where applicable)
    3. All endpoints have response schemas

    Args:
        base_url: Base URL of the API server

    Raises:
        SystemExit: If validation fails
    """
    openapi_url = f"{base_url}/openapi.json"

    # Check 1: Fetch OpenAPI spec
    try:
        response = requests.get(openapi_url, timeout=10)
        response.raise_for_status()
        spec = response.json()
    except requests.exceptions.RequestException as e:
        print(f"\n❌ ERROR: Could not fetch OpenAPI spec from {openapi_url}")
        print(f"   Reason: {e}")
        sys.exit(1)
    except ValueError as e:
        print(f"\n❌ ERROR: Invalid JSON in OpenAPI spec from {openapi_url}")
        print(f"   Reason: {e}")
        sys.exit(1)
    # TODO: Add JsonDecodeError handling

    # Validate the spec structure
    if "paths" not in spec:
        print(f"\n❌ ERROR: OpenAPI spec missing 'paths' key")
        sys.exit(1)

    # Check 2 & 3: Validate endpoints
    errors = []
    paths = spec.get("paths", {})

    for path, path_item in paths.items():
        for method in ["get", "post", "put", "delete"]:
            if method not in path_item:
                continue

            operation = path_item[method]

            # Check request body examples for POST/PUT/DELETE
            if method in ["post", "put", "delete"]:
                error = check_request_body_has_example(method, path, operation)
                if error:
                    errors.append(error)

            # Check response schemas for all methods
            error = check_operation_has_responses(method, path, operation)
            if error:
                errors.append(error)
                continue

            responses = operation.get("responses", {})
            for status_code, response_obj in responses.items():
                error = check_response_has_example(
                    method, path, status_code, response_obj
                )
                if error:
                    errors.append(error)

    # Report errors
    if errors:
        print(f"\n❌ ERROR: OpenAPI spec validation failed")
        print(f"\nThe following endpoints are missing required examples:")
        for error in errors:
            print(error)
        print(
            f"\npytest-openapi requires examples for all endpoints to generate tests."
        )
        sys.exit(1)

    print(f"\n✅ OpenAPI spec validated successfully from {openapi_url}")
    print(f"   Found {len(paths)} path(s)")
