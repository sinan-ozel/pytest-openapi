"""OpenAPI contract testing - execute tests against live endpoints."""

import requests


def compare_responses(expected, actual):
    """
    Compare expected and actual responses with detailed error messages.

    Args:
        expected: Expected response (from OpenAPI example)
        actual: Actual response from API

    Returns:
        tuple: (matches: bool, error_message: str or None)
    """
    if expected == actual:
        return True, None

    # Check for missing keys in actual
    if isinstance(expected, dict) and isinstance(actual, dict):
        for key in expected:
            if key not in actual:
                return (
                    False,
                    f"Missing key in actual response: '{key}'. Expected: {expected}, Actual: {actual}",
                )

        # Check for extra keys in actual
        for key in actual:
            if key not in expected:
                return (
                    False,
                    f"Extra key in actual response: '{key}'. Expected: {expected}, Actual: {actual}",
                )

        # Check for type mismatches
        for key in expected:
            if key in actual:
                expected_type = type(expected[key]).__name__
                actual_type = type(actual[key]).__name__
                if expected_type != actual_type:
                    return (
                        False,
                        f"Type mismatch for key '{key}': expected {expected_type}, got {actual_type}. "
                        f"Expected value: {expected[key]}, Actual value: {actual[key]}",
                    )

                # Recursively check nested dicts/lists
                if isinstance(expected[key], (dict, list)):
                    matches, error = compare_responses(
                        expected[key], actual[key]
                    )
                    if not matches:
                        return False, error

    return False, f"Response mismatch.\nExpected: {expected}\nActual: {actual}"


def test_get_endpoint(base_url, path, operation):
    """
    Test a GET endpoint using the example from the OpenAPI spec.

    Args:
        base_url: Base URL of the API server
        path: API endpoint path
        operation: OpenAPI operation object

    Returns:
        tuple: (success: bool, error_message: str or None)
    """
    url = f"{base_url}{path}"

    # Get the expected response example for 200 status
    responses = operation.get("responses", {})
    response_200 = responses.get("200", {})
    content = response_200.get("content", {})

    expected_response = None
    for media_type, media_obj in content.items():
        if "example" in media_obj:
            expected_response = media_obj["example"]
            break

    if expected_response is None:
        return False, "No example found for 200 response"

    # Make the GET request
    try:
        response = requests.get(url, timeout=10)
    except requests.exceptions.RequestException as e:
        return False, f"Request failed: {e}"

    # Check status code
    if response.status_code != 200:
        return (
            False,
            f"Expected status 200, got {response.status_code}. Response: {response.text}",
        )

    # Check response matches example
    actual_response = response.json()
    matches, error = compare_responses(expected_response, actual_response)
    if not matches:
        return False, error

    return True, None


def test_post_endpoint(base_url, path, operation):
    """
    Test a POST endpoint using the example from the OpenAPI spec.

    Args:
        base_url: Base URL of the API server
        path: API endpoint path
        operation: OpenAPI operation object

    Returns:
        tuple: (success: bool, error_message: str or None)
    """
    url = f"{base_url}{path}"

    # Get the request body example
    request_body = operation.get("requestBody", {})
    request_content = request_body.get("content", {})

    request_example = None
    for media_type, media_obj in request_content.items():
        if "example" in media_obj:
            request_example = media_obj["example"]
            break

    if request_example is None:
        return False, "No request body example found"

    # Get the expected response example for 200 status
    responses = operation.get("responses", {})
    response_200 = responses.get("200", {}) or responses.get("201", {})
    content = response_200.get("content", {})

    expected_response = None
    for media_type, media_obj in content.items():
        if "example" in media_obj:
            expected_response = media_obj["example"]
            break

    if expected_response is None:
        return False, "No example found for 200/201 response"

    # Make the POST request
    try:
        response = requests.post(url, json=request_example, timeout=10)
    except requests.exceptions.RequestException as e:
        return False, f"Request failed: {e}"

    # Check status code (accept both 200 and 201 for POST)
    if response.status_code not in [200, 201]:
        return (
            False,
            f"Expected status 200/201, got {response.status_code}. Response: {response.text}",
        )

    # Check response matches example
    actual_response = response.json()
    matches, error = compare_responses(expected_response, actual_response)
    if not matches:
        return False, error

    return True, None


def test_put_endpoint(base_url, path, operation):
    """
    Test a PUT endpoint using the example from the OpenAPI spec.

    Args:
        base_url: Base URL of the API server
        path: API endpoint path (may contain path parameters)
        operation: OpenAPI operation object

    Returns:
        tuple: (success: bool, error_message: str or None)
    """
    # Get the request body example
    request_body = operation.get("requestBody", {})
    request_content = request_body.get("content", {})

    request_example = None
    for media_type, media_obj in request_content.items():
        if "example" in media_obj:
            request_example = media_obj["example"]
            break

    if request_example is None:
        return False, "No request body example found"

    # Get the expected response example for 200 status
    responses = operation.get("responses", {})
    response_200 = responses.get("200", {})
    content = response_200.get("content", {})

    expected_response = None
    for media_type, media_obj in content.items():
        if "example" in media_obj:
            expected_response = media_obj["example"]
            break

    if expected_response is None:
        return False, "No example found for 200 response"

    # Replace path parameters with values from the response example
    url = f"{base_url}{path}"
    if "{" in path:
        import re

        # Get path parameters from operation definition
        parameters = operation.get("parameters", [])

        for match in re.finditer(r"\{(\w+)\}", path):
            param_name = match.group(1)

            # Try to find the value in the response example
            # Common mappings: item_id -> id, user_id -> id, etc.
            value = None

            if param_name in expected_response:
                value = expected_response[param_name]
            elif param_name.endswith("_id") and "id" in expected_response:
                # Map item_id -> id, user_id -> id, etc.
                value = expected_response["id"]
            elif "id" in expected_response:
                # Default to using the id field
                value = expected_response["id"]
            else:
                # Use a default test value
                value = 1

            url = url.replace(f"{{{param_name}}}", str(value))

    # Make the PUT request
    try:
        response = requests.put(url, json=request_example, timeout=10)
    except requests.exceptions.RequestException as e:
        return False, f"Request failed: {e}"

    # Check status code
    if response.status_code != 200:
        return (
            False,
            f"Expected status 200, got {response.status_code}. Response: {response.text}",
        )

    # Check response matches example
    actual_response = response.json()
    matches, error = compare_responses(expected_response, actual_response)
    if not matches:
        return False, error

    return True, None


def test_delete_endpoint(base_url, path, operation):
    """
    Test a DELETE endpoint using the example from the OpenAPI spec.

    Args:
        base_url: Base URL of the API server
        path: API endpoint path (may contain path parameters)
        operation: OpenAPI operation object

    Returns:
        tuple: (success: bool, error_message: str or None)
    """
    # For DELETE, we need to get path parameters from the 200 response example
    # (if it exists) or from a 404 response example
    responses = operation.get("responses", {})

    # Try to find an example with path parameters
    response_example = None
    for status_code in ["200", "204", "404"]:
        resp_obj = responses.get(status_code, {})
        content = resp_obj.get("content", {})
        for media_type, media_obj in content.items():
            if "example" in media_obj:
                response_example = media_obj["example"]
                break
        if response_example:
            break

    # Replace path parameters with values from the example
    url = f"{base_url}{path}"
    if "{" in path:
        import re

        # For DELETE, use a hardcoded ID if no example provides it
        # This is a simplification - in reality we might need to create a resource first
        for match in re.finditer(r"\{(\w+)\}", path):
            param_name = match.group(1)

            # Try to find the value in the response example
            # Common mappings: item_id -> id, user_id -> id, etc.
            param_value = None

            if response_example and isinstance(response_example, dict):
                if param_name in response_example:
                    param_value = response_example[param_name]
                elif param_name.endswith("_id") and "id" in response_example:
                    # Map item_id -> id, user_id -> id, etc.
                    param_value = response_example["id"]
                elif "id" in response_example:
                    # Default to using the id field
                    param_value = response_example["id"]

            # Default test value if not found
            if param_value is None:
                param_value = 1

            url = url.replace(f"{{{param_name}}}", str(param_value))

    # Make the DELETE request
    try:
        response = requests.delete(url, timeout=10)
    except requests.exceptions.RequestException as e:
        return False, f"Request failed: {e}"

    # Check status code (accept 200 or 204 for successful DELETE)
    if response.status_code not in [200, 204]:
        return (
            False,
            f"Expected status 200/204, got {response.status_code}. Response: {response.text}",
        )

    return True, None
