"""OpenAPI contract testing - execute tests against live endpoints."""

import json
import requests


# Global list to store test reports
test_reports = []


def make_request(method, url, json=None, timeout=10):
    """
    Wrapper for HTTP requests that logs all requests and responses for reporting.

    Args:
        method: HTTP method (GET, POST, PUT, DELETE)
        url: Full URL to request
        json: Optional JSON body for request
        timeout: Request timeout in seconds

    Returns:
        requests.Response object
    """
    # Make the actual request
    if method.upper() == "GET":
        response = requests.get(url, timeout=timeout)
    elif method.upper() == "POST":
        response = requests.post(url, json=json, timeout=timeout)
    elif method.upper() == "PUT":
        response = requests.put(url, json=json, timeout=timeout)
    elif method.upper() == "DELETE":
        response = requests.delete(url, timeout=timeout)
    else:
        raise ValueError(f"Unsupported HTTP method: {method}")

    return response


def log_test_result(method, path, request_body, expected_status, expected_body, actual_status, actual_body, success, error_message=None):
    """
    Log a test result for the final report.

    Args:
        method: HTTP method (GET, POST, PUT, DELETE)
        path: URL path
        request_body: Request body (if any)
        expected_status: Expected HTTP status code
        expected_body: Expected response body
        actual_status: Actual HTTP status code
        actual_body: Actual response body
        success: Whether the test passed
        error_message: Error message if test failed
    """
    report = {
        "method": method,
        "path": path,
        "request_body": request_body,
        "expected_status": expected_status,
        "expected_body": expected_body,
        "actual_status": actual_status,
        "actual_body": actual_body,
        "success": success,
        "error_message": error_message
    }
    test_reports.append(report)


def get_test_report():
    """
    Generate a human-readable test report.

    Returns:
        str: Formatted report of all tests
    """
    if not test_reports:
        return "No tests have been run yet."

    report_lines = []
    report_lines.append("=" * 80)
    report_lines.append("OpenAPI Contract Test Report")
    report_lines.append("=" * 80)
    report_lines.append("")

    for i, test in enumerate(test_reports, 1):
        status_symbol = "✅" if test["success"] else "❌"
        report_lines.append(f"Test #{i} {status_symbol}")
        report_lines.append(f"{test['method']} {test['path']}")

        if test["request_body"] is not None:
            formatted_request = json.dumps(test["request_body"], indent=2)
            report_lines.append(f"Requested:")
            for line in formatted_request.split('\n'):
                report_lines.append(f"  {line}")

        report_lines.append("")

        # Format expected body
        if test["expected_body"] == "" or test["expected_body"] is None:
            expected_body_str = "(empty)"
        else:
            try:
                expected_body_str = json.dumps(test["expected_body"], indent=2)
                expected_body_str = "\n  ".join(expected_body_str.split('\n'))
            except (TypeError, ValueError):
                expected_body_str = str(test["expected_body"])

        # Format actual body
        if test["actual_body"] == "" or test["actual_body"] is None:
            actual_body_str = "(empty)"
        else:
            try:
                actual_body_str = json.dumps(test["actual_body"], indent=2)
                actual_body_str = "\n  ".join(actual_body_str.split('\n'))
            except (TypeError, ValueError):
                actual_body_str = str(test["actual_body"])

        report_lines.append(f"Expected {test['expected_status']}")
        report_lines.append(f"  {expected_body_str}")
        report_lines.append("")
        report_lines.append(f"Actual {test['actual_status']}")
        report_lines.append(f"  {actual_body_str}")

        if not test["success"] and test["error_message"]:
            report_lines.append("")
            report_lines.append(f"Error: {test['error_message']}")

        report_lines.append("")
        report_lines.append("-" * 80)
        report_lines.append("")

    return "\n".join(report_lines)


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
        response = make_request("GET", url)
    except requests.exceptions.RequestException as e:
        error_msg = f"Request failed: {e}"
        log_test_result("GET", path, None, 200, expected_response, None, None, False, error_msg)
        return False, error_msg

    # Check status code
    actual_response = response.json() if response.status_code == 200 else response.text

    if response.status_code != 200:
        error_msg = f"Expected status 200, got {response.status_code}. Response: {response.text}"
        log_test_result("GET", path, None, 200, expected_response, response.status_code, actual_response, False, error_msg)
        return False, error_msg

    # Check response matches example
    matches, error = compare_responses(expected_response, actual_response)
    if not matches:
        log_test_result("GET", path, None, 200, expected_response, response.status_code, actual_response, False, error)
        return False, error

    log_test_result("GET", path, None, 200, expected_response, response.status_code, actual_response, True)
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
    expected_status = 201 if "201" in responses else 200
    for media_type, media_obj in content.items():
        if "example" in media_obj:
            expected_response = media_obj["example"]
            break

    if expected_response is None:
        return False, "No example found for 200/201 response"

    # Make the POST request
    try:
        response = make_request("POST", url, json=request_example)
    except requests.exceptions.RequestException as e:
        error_msg = f"Request failed: {e}"
        log_test_result("POST", path, request_example, expected_status, expected_response, None, None, False, error_msg)
        return False, error_msg

    # Check status code (accept both 200 and 201 for POST)
    actual_response = response.json() if response.status_code in [200, 201] else response.text

    if response.status_code not in [200, 201]:
        error_msg = f"Expected status 200/201, got {response.status_code}. Response: {response.text}"
        log_test_result("POST", path, request_example, expected_status, expected_response, response.status_code, actual_response, False, error_msg)
        return False, error_msg

    # Check response matches example
    matches, error = compare_responses(expected_response, actual_response)
    if not matches:
        log_test_result("POST", path, request_example, expected_status, expected_response, response.status_code, actual_response, False, error)
        return False, error

    log_test_result("POST", path, request_example, expected_status, expected_response, response.status_code, actual_response, True)
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
    resolved_path = path
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
            resolved_path = resolved_path.replace(f"{{{param_name}}}", str(value))

    # Make the PUT request
    try:
        response = make_request("PUT", url, json=request_example)
    except requests.exceptions.RequestException as e:
        error_msg = f"Request failed: {e}"
        log_test_result("PUT", resolved_path, request_example, 200, expected_response, None, None, False, error_msg)
        return False, error_msg

    # Check status code
    actual_response = response.json() if response.status_code == 200 else response.text

    if response.status_code != 200:
        error_msg = f"Expected status 200, got {response.status_code}. Response: {response.text}"
        log_test_result("PUT", resolved_path, request_example, 200, expected_response, response.status_code, actual_response, False, error_msg)
        return False, error_msg

    # Check response matches example
    matches, error = compare_responses(expected_response, actual_response)
    if not matches:
        log_test_result("PUT", resolved_path, request_example, 200, expected_response, response.status_code, actual_response, False, error)
        return False, error

    log_test_result("PUT", resolved_path, request_example, 200, expected_response, response.status_code, actual_response, True)
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
    expected_status = None
    expected_body = None

    for status_code in ["200", "204", "404"]:
        resp_obj = responses.get(status_code, {})
        if status_code in ["200", "204"]:
            expected_status = int(status_code)
        content = resp_obj.get("content", {})
        for media_type, media_obj in content.items():
            if "example" in media_obj:
                response_example = media_obj["example"]
                expected_body = response_example
                break
        if response_example:
            break

    # If no expected body found (common for 204 responses), use empty string
    if expected_status is None:
        expected_status = 204
    if expected_body is None:
        expected_body = ""

    # Replace path parameters with values from the example
    url = f"{base_url}{path}"
    resolved_path = path
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
            resolved_path = resolved_path.replace(f"{{{param_name}}}", str(param_value))

    # Make the DELETE request
    try:
        response = make_request("DELETE", url)
    except requests.exceptions.RequestException as e:
        error_msg = f"Request failed: {e}"
        log_test_result("DELETE", resolved_path, None, expected_status, expected_body, None, None, False, error_msg)
        return False, error_msg

    # Check status code (accept 200 or 204 for successful DELETE)
    actual_response = ""
    if response.status_code == 200 and response.text:
        try:
            actual_response = response.json()
        except:
            actual_response = response.text

    if response.status_code not in [200, 204]:
        error_msg = f"Expected status 200/204, got {response.status_code}. Response: {response.text}"
        log_test_result("DELETE", resolved_path, None, expected_status, expected_body, response.status_code, actual_response, False, error_msg)
        return False, error_msg

    log_test_result("DELETE", resolved_path, None, expected_status, expected_body, response.status_code, actual_response, True)
    return True, None
