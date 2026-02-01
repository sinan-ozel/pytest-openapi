"""OpenAPI contract testing - execute tests against live endpoints."""

import json

import requests

from .case_generator import generate_test_cases_for_schema

# Global list to store test reports
test_reports = []


def make_request(method, url, json=None, timeout=10):
    """Wrapper for HTTP requests that logs all requests and responses
    for reporting.

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


def log_test_result(
    method,
    path,
    request_body,
    expected_status,
    expected_body,
    actual_status,
    actual_body,
    success,
    error_message=None,
    test_case_origin=None,
    documented_statuses=None,
):
    """Log a test result for the final report.

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
        test_case_origin: Origin of test case ('example' or 'generated')
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
        "error_message": error_message,
        "test_case_origin": test_case_origin,
    }
    # Attach documented status codes (if provided) to the report for clearer expectations
    report["documented_statuses"] = (
        list(documented_statuses) if documented_statuses else []
    )
    test_reports.append(report)


def get_test_report():
    """Generate a human-readable test report.

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

        # Display test case origin if available
        if test.get("test_case_origin"):
            origin = test["test_case_origin"]
            if origin == "example":
                report_lines.append("📋 Test case from OpenAPI example")
            elif origin == "generated":
                report_lines.append("🔧 Test case generated from schema")

        report_lines.append(f"{test['method']} {test['path']}")

        if test["request_body"] is not None:
            formatted_request = json.dumps(test["request_body"], indent=2)
            report_lines.append("Requested:")
            for line in formatted_request.split("\n"):
                report_lines.append(f"  {line}")

        report_lines.append("")

        # Format expected body
        if test["expected_body"] == "" or test["expected_body"] is None:
            expected_body_str = "(empty)"
        else:
            try:
                expected_body_str = json.dumps(test["expected_body"], indent=2)
                expected_body_str = "\n  ".join(expected_body_str.split("\n"))
            except (TypeError, ValueError):
                expected_body_str = str(test["expected_body"])

        # Format actual body
        if test["actual_body"] == "" or test["actual_body"] is None:
            actual_body_str = "(empty)"
        else:
            try:
                actual_body_str = json.dumps(test["actual_body"], indent=2)
                actual_body_str = "\n  ".join(actual_body_str.split("\n"))
            except (TypeError, ValueError):
                actual_body_str = str(test["actual_body"])

        # Show expected status and any other documented statuses (e.g., 501) as accepted
        documented = test.get("documented_statuses", []) or []
        expected_primary = test["expected_status"]
        statuses = [str(expected_primary)] + [
            str(s) for s in documented if s != expected_primary
        ]
        expected_display = " or ".join(statuses)
        report_lines.append(f"Expected {expected_display}")
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


def get_test_report_markdown():
    """Generate a Markdown-formatted test report.

    Returns:
        str: Markdown formatted report of all tests
    """
    if not test_reports:
        return "No tests have been run yet."

    report_lines = []
    report_lines.append("# OpenAPI Contract Test Report")
    report_lines.append("")

    # Summary statistics
    total_tests = len(test_reports)
    passed_tests = sum(1 for test in test_reports if test["success"])
    failed_tests = total_tests - passed_tests

    report_lines.append("## Summary")
    report_lines.append("")
    report_lines.append(f"- **Total Tests:** {total_tests}")
    report_lines.append(f"- **Passed:** ✅ {passed_tests}")
    report_lines.append(f"- **Failed:** ❌ {failed_tests}")
    report_lines.append("")
    report_lines.append("---")
    report_lines.append("")

    for i, test in enumerate(test_reports, 1):
        status_symbol = "✅" if test["success"] else "❌"
        report_lines.append(f"## Test #{i} {status_symbol}")
        report_lines.append("")

        # Display test case origin if available
        if test.get("test_case_origin"):
            origin = test["test_case_origin"]
            if origin == "example":
                report_lines.append("📋 *Test case from OpenAPI example*")
            elif origin == "generated":
                report_lines.append("🔧 *Test case generated from schema*")
            report_lines.append("")

        report_lines.append(
            f"**Endpoint:** `{test['method'].upper()} {test['path']}`"
        )
        report_lines.append("")

        if test["request_body"] is not None:
            formatted_request = json.dumps(test["request_body"], indent=2)
            report_lines.append("### Request Body")
            report_lines.append("")
            report_lines.append("```json")
            report_lines.append(formatted_request)
            report_lines.append("```")
            report_lines.append("")

        # Format expected body
        if test["expected_body"] == "" or test["expected_body"] is None:
            expected_body_str = "*(empty)*"
        else:
            try:
                expected_body_str = json.dumps(test["expected_body"], indent=2)
            except (TypeError, ValueError):
                expected_body_str = str(test["expected_body"])

        # Format actual body
        if test["actual_body"] == "" or test["actual_body"] is None:
            actual_body_str = "*(empty)*"
        else:
            try:
                actual_body_str = json.dumps(test["actual_body"], indent=2)
            except (TypeError, ValueError):
                actual_body_str = str(test["actual_body"])

        report_lines.append("### Expected Response")
        report_lines.append("")
        # Include documented statuses (for example, 501) alongside primary expected status
        documented = test.get("documented_statuses", []) or []
        expected_primary = test["expected_status"]
        statuses = [str(expected_primary)] + [
            str(s) for s in documented if s != expected_primary
        ]
        expected_display = " or ".join(statuses)
        report_lines.append(f"**Status:** `{expected_display}`")
        report_lines.append("")
        if expected_body_str != "*(empty)*":
            report_lines.append("```json")
            report_lines.append(expected_body_str)
            report_lines.append("```")
        else:
            report_lines.append(expected_body_str)
        report_lines.append("")

        report_lines.append("### Actual Response")
        report_lines.append("")
        report_lines.append(f"**Status:** `{test['actual_status']}`")
        report_lines.append("")
        if actual_body_str != "*(empty)*":
            report_lines.append("```json")
            report_lines.append(actual_body_str)
            report_lines.append("```")
        else:
            report_lines.append(actual_body_str)
        report_lines.append("")

        if not test["success"] and test["error_message"]:
            report_lines.append("### ❌ Error")
            report_lines.append("")
            report_lines.append("```")
            report_lines.append(test["error_message"])
            report_lines.append("```")
            report_lines.append("")

        report_lines.append("---")
        report_lines.append("")

    return "\n".join(report_lines)


def contains_invalid_enum_value(schema, data, path=""):
    """Check if data contains any invalid enum values according to
    schema.

    Args:
        schema: OpenAPI schema object
        data: Request/response data to check
        path: Current path in object (for tracking)

    Returns:
        bool: True if data contains an invalid enum value, False otherwise
    """
    if not isinstance(schema, dict):
        return False

    schema_type = schema.get("type")

    # Check if this field has an enum and the value is invalid
    if "enum" in schema:
        allowed_values = schema["enum"]
        # For scalar values (string, int, float, bool), check directly
        if not isinstance(data, (dict, list)):
            if data not in allowed_values:
                return True

    # Recursively check nested objects
    if schema_type == "object" and isinstance(data, dict):
        properties = schema.get("properties", {})
        for prop, prop_schema in properties.items():
            if prop in data:
                if contains_invalid_enum_value(
                    prop_schema, data[prop], f"{path}.{prop}" if path else prop
                ):
                    return True

    # Check array items
    elif schema_type == "array" and isinstance(data, list):
        items_schema = schema.get("items", {})
        for i, item in enumerate(data):
            if contains_invalid_enum_value(items_schema, item, f"{path}[{i}]"):
                return True

    return False


def validate_against_schema(schema, actual, path=""):
    """Validate actual response against JSON schema.

    Args:
        schema: JSON schema object
        actual: Actual response data
        path: Current path in object (for error messages)

    Returns:
        tuple: (valid: bool, error_message: str or None)
    """
    schema_type = schema.get("type")

    # Handle nullable fields (OpenAPI 3.0 uses "nullable": true, OpenAPI 3.1 uses type: ["string", "null"])
    is_nullable = schema.get("nullable", False)
    if isinstance(schema_type, list):
        # OpenAPI 3.1 style: type: ["string", "null"]
        if "null" in schema_type and actual is None:
            return True, None
        # Filter out "null" and get the actual type
        non_null_types = [t for t in schema_type if t != "null"]
        if len(non_null_types) == 1:
            schema_type = non_null_types[0]
        elif len(non_null_types) > 1:
            # Multiple non-null types - try each one
            for possible_type in non_null_types:
                temp_schema = schema.copy()
                temp_schema["type"] = possible_type
                valid, _ = validate_against_schema(temp_schema, actual, path)
                if valid:
                    return True, None
            return (
                False,
                f"{path}: Value does not match any of the allowed types: {non_null_types}",
            )
    elif is_nullable and actual is None:
        # OpenAPI 3.0 style: nullable: true
        return True, None

    # Check enum values before type validation
    if "enum" in schema:
        allowed_values = schema["enum"]
        if actual not in allowed_values:
            return (
                False,
                f"{path}: Value '{actual}' is not one of the allowed enum values: {allowed_values}",
            )

    # Check type
    if schema_type == "object":
        if not isinstance(actual, dict):
            return (
                False,
                f"{path}: Expected object, got {type(actual).__name__}",
            )

        # Check required properties
        required = schema.get("required", [])
        for prop in required:
            if prop not in actual:
                return False, f"{path}: Missing required property '{prop}'"

        # Validate properties
        properties = schema.get("properties", {})
        for prop, prop_schema in properties.items():
            if prop in actual:
                valid, error = validate_against_schema(
                    prop_schema,
                    actual[prop],
                    f"{path}.{prop}" if path else prop,
                )
                if not valid:
                    return False, error

    elif schema_type == "array":
        if not isinstance(actual, list):
            return False, f"{path}: Expected array, got {type(actual).__name__}"

        # Validate items
        items_schema = schema.get("items", {})
        for i, item in enumerate(actual):
            valid, error = validate_against_schema(
                items_schema, item, f"{path}[{i}]"
            )
            if not valid:
                return False, error

    elif schema_type == "string":
        if not isinstance(actual, str):
            return (
                False,
                f"{path}: Expected string, got {type(actual).__name__}",
            )

    elif schema_type == "number":
        if not isinstance(actual, (int, float)):
            return (
                False,
                f"{path}: Expected number, got {type(actual).__name__}",
            )

    elif schema_type == "integer":
        if not isinstance(actual, int) or isinstance(actual, bool):
            return (
                False,
                f"{path}: Expected integer, got {type(actual).__name__}",
            )

    elif schema_type == "boolean":
        if not isinstance(actual, bool):
            return (
                False,
                f"{path}: Expected boolean, got {type(actual).__name__}",
            )

    return True, None


def compare_responses(expected, actual, strict=True):
    """Compare expected and actual responses with detailed error
    messages.

    Args:
        expected: Expected response (from OpenAPI example)
        actual: Actual response from API
        strict: If False, only validate structure/types (lenient mode)

    Returns:
        tuple: (matches: bool, error_message: str or None)
    """
    if expected == actual:
        return True, None

    # In lenient mode, only check structure and types, not exact values
    if not strict:
        return compare_structure(expected, actual)

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

        # If we've checked keys and types and any nested structures
        # recursively without finding a mismatch, consider this a match
        return True, None

    # For lists, check element-wise types/structure
    if isinstance(expected, list) and isinstance(actual, list):
        if len(expected) != len(actual):
            return (
                False,
                f"List length mismatch: expected {len(expected)}, got {len(actual)}. Expected: {expected}, Actual: {actual}",
            )
        for e_item, a_item in zip(expected, actual):
            matches, error = compare_responses(e_item, a_item)
            if not matches:
                return False, error
        return True, None

    return False, f"Response mismatch.\nExpected: {expected}\nActual: {actual}"


def compare_structure(expected, actual):
    """Compare structure and types only (lenient mode).

    Args:
        expected: Expected response (used for structure reference)
        actual: Actual response from API

    Returns:
        tuple: (matches: bool, error_message: str or None)
    """
    # Check types match
    if type(expected).__name__ != type(actual).__name__:
        return (
            False,
            f"Type mismatch: expected {type(expected).__name__}, got {type(actual).__name__}",
        )

    if isinstance(expected, dict):
        # Check all expected keys exist
        for key in expected:
            if key not in actual:
                return False, f"Missing key in actual response: '{key}'"

        # Recursively check structure of nested values
        for key in expected:
            if key in actual:
                matches, error = compare_structure(expected[key], actual[key])
                if not matches:
                    return False, error

        return True, None

    elif isinstance(expected, list):
        # For arrays, just check that element types are compatible
        # Don't enforce length or exact values
        if len(expected) > 0 and len(actual) > 0:
            # Check first element structure
            matches, error = compare_structure(expected[0], actual[0])
            if not matches:
                return False, f"Array element structure mismatch: {error}"
        return True, None

    # For primitives, just check type (already done above)
    return True, None


def test_get_endpoint(
    base_url, path, operation, strict_examples=True, timeout=10
):
    """Test a GET endpoint using the example from the OpenAPI spec.

    Args:
        base_url: Base URL of the API server
        path: API endpoint path
        operation: OpenAPI operation object        strict_examples: If True, strictly match example responses; if False, only validate structure
    Returns:
        tuple: (success: bool, error_message: str or None)
    """
    url = f"{base_url}{path}"

    # Get the expected response from examples or generate from schema
    responses = operation.get("responses", {})
    response_200 = responses.get("200", {})
    content = response_200.get("content", {})

    # Get all documented response status codes
    documented_statuses = set()
    for status_code in responses.keys():
        try:
            documented_statuses.add(int(status_code))
        except (ValueError, TypeError):
            pass  # Skip non-numeric status codes like 'default'

    expected_response = None
    response_schema = None
    is_example_based = False

    for media_type, media_obj in content.items():
        if "example" in media_obj:
            expected_response = media_obj["example"]
            is_example_based = True
            # Also extract schema if present for schema-generated tests
            if "schema" in media_obj:
                response_schema = media_obj["schema"]
            break
        elif "examples" in media_obj:
            examples = media_obj["examples"]
            if examples:
                first_example = next(iter(examples.values()))
                expected_response = first_example.get("value")
                is_example_based = True
                # Also extract schema if present for schema-generated tests
                if "schema" in media_obj:
                    response_schema = media_obj["schema"]
                break

    # We are opinionated: examples are required
    if expected_response is None:
        return (
            False,
            "No example found for 200 response. Examples are required.",
        )

    # Make the GET request
    try:
        response = make_request("GET", url, timeout=timeout)
    except requests.exceptions.RequestException as e:
        error_msg = f"Request failed: {e}"
        log_test_result(
            "GET",
            path,
            None,
            200,
            expected_response,
            None,
            None,
            False,
            error_msg,
            "example",
            documented_statuses=documented_statuses,
        )
        return False, error_msg

    # Check status code
    actual_response = (
        response.json() if response.status_code == 200 else response.text
    )

    # In lenient mode, accept any documented status code
    if not strict_examples and response.status_code in documented_statuses:
        # Get the response schema/example for the actual status code
        actual_status_response = responses.get(str(response.status_code), {})
        actual_content = actual_status_response.get("content", {})
        actual_expected_response = None
        actual_response_schema = None

        for media_type, media_obj in actual_content.items():
            if "example" in media_obj:
                actual_expected_response = media_obj["example"]
            if "schema" in media_obj:
                actual_response_schema = media_obj["schema"]
            break

        # Parse JSON response if possible
        try:
            if response.text:
                actual_response = response.json()
        except Exception:
            pass

        # Validate against the actual status code's schema
        if actual_response_schema:
            matches, error = validate_against_schema(
                actual_response_schema, actual_response
            )
        elif actual_expected_response:
            matches, error = compare_responses(
                actual_expected_response, actual_response, strict=False
            )
        else:
            # No schema or example for this status, just accept it
            matches, error = True, None

        if matches:
            log_test_result(
                "GET",
                path,
                None,
                200,
                expected_response,
                response.status_code,
                actual_response,
                True,
                None,
                "example",
                documented_statuses=documented_statuses,
            )
            return True, None
        else:
            log_test_result(
                "GET",
                path,
                None,
                200,
                expected_response,
                response.status_code,
                actual_response,
                False,
                error,
                "example",
                documented_statuses=documented_statuses,
            )
            return False, error

    # Accept 501 (Not Implemented) as valid if documented (for strict mode)
    if response.status_code == 501 and 501 in documented_statuses:
        log_test_result(
            "GET",
            path,
            None,
            200,
            expected_response,
            response.status_code,
            actual_response,
            True,
            None,
            "example",
            documented_statuses=documented_statuses,
        )
        return True, None

    if response.status_code != 200:
        error_msg = f"Expected status 200, got {response.status_code}. Response: {response.text}"
        log_test_result(
            "GET",
            path,
            None,
            200,
            expected_response,
            response.status_code,
            actual_response,
            False,
            error_msg,
            "example",
            documented_statuses=documented_statuses,
        )
        return False, error_msg

    # Check response matches example or schema
    if is_example_based:
        # Example-based test: use strict or lenient matching based on flag
        matches, error = compare_responses(
            expected_response, actual_response, strict=strict_examples
        )
    elif response_schema:
        # Schema-generated test: always use schema validation
        matches, error = validate_against_schema(
            response_schema, actual_response
        )
    else:
        # Fallback to strict comparison
        matches, error = compare_responses(
            expected_response, actual_response, strict=True
        )

    if not matches:
        log_test_result(
            "GET",
            path,
            None,
            200,
            expected_response,
            response.status_code,
            actual_response,
            False,
            error,
            "example",
            documented_statuses=documented_statuses,
        )
        return False, error

    log_test_result(
        "GET",
        path,
        None,
        200,
        expected_response,
        response.status_code,
        actual_response,
        True,
        None,
        "example",
    )
    return True, None


def test_post_endpoint(
    base_url, path, operation, strict_examples=True, timeout=10
):
    """Test a POST endpoint using examples from OpenAPI spec AND
    generated test cases from schema.

    Args:
        base_url: Base URL of the API server
        path: API endpoint path
        operation: OpenAPI operation object
        strict_examples: If True, strictly match example responses; if False, only validate structure

    Returns:
        tuple: (success: bool, error_message: str or None)
    """
    url = f"{base_url}{path}"

    # Collect ALL test cases: both from examples AND generated from schema
    # Track which are example-based vs schema-generated
    request_test_cases = []
    test_case_origins = (
        []
    )  # Track if each test case is 'example' or 'generated'
    warnings = []

    request_body = operation.get("requestBody", {})
    request_content = request_body.get("content", {})

    for media_type, media_obj in request_content.items():
        # Collect explicit examples
        if "example" in media_obj:
            request_test_cases.append(media_obj["example"])
            test_case_origins.append("example")
        if "examples" in media_obj:
            examples_dict = media_obj["examples"]
            for ex_name, ex_obj in examples_dict.items():
                if "value" in ex_obj:
                    request_test_cases.append(ex_obj["value"])
                    test_case_origins.append("example")

        # Also generate test cases from schema
        if "schema" in media_obj:
            schema = media_obj["schema"]
            generated, warning = generate_test_cases_for_schema(
                schema, "request_body"
            )
            if warning:
                if isinstance(warning, list):
                    warnings.extend(warning)
                else:
                    warnings.append(warning)
            for gen_case in generated:
                request_test_cases.append(gen_case)
                test_case_origins.append("generated")
        break

    if not request_test_cases:
        return False, "No request body examples or schema found"

    # Print warnings if any
    for warning in warnings:
        print(f"\n{warning}")

    # Get expected response - collect examples AND generated test cases
    responses = operation.get("responses", {})
    response_200 = responses.get("200", {}) or responses.get("201", {})
    content = response_200.get("content", {})

    expected_response = None
    response_schema = None
    response_is_example_based = False
    expected_status = 201 if "201" in responses else 200

    # Get all documented response status codes
    documented_statuses = set()
    for status_code in responses.keys():
        try:
            documented_statuses.add(int(status_code))
        except (ValueError, TypeError):
            pass  # Skip non-numeric status codes like 'default'

    for media_type, media_obj in content.items():
        # Prefer explicit example
        if "example" in media_obj:
            expected_response = media_obj["example"]
            response_is_example_based = True
            # Also extract schema if present for schema-generated tests
            if "schema" in media_obj:
                response_schema = media_obj["schema"]
            break
        elif "examples" in media_obj:
            examples_dict = media_obj["examples"]
            if examples_dict:
                first_example = next(iter(examples_dict.values()))
                expected_response = first_example.get("value")
                response_is_example_based = True
                # Also extract schema if present for schema-generated tests
                if "schema" in media_obj:
                    response_schema = media_obj["schema"]
                break

    # We are opinionated: examples are required
    if expected_response is None:
        return (
            False,
            "No example found for 200/201 response. Examples are required.",
        )

    # Test with all collected test cases (examples + generated)
    errors = []
    for request_test_case, test_origin in zip(
        request_test_cases, test_case_origins
    ):
        # Check if this request contains an invalid enum value
        request_schema = None
        for media_type, media_obj in request_content.items():
            if "schema" in media_obj:
                request_schema = media_obj["schema"]
                break

        is_negative_test = False
        if request_schema:
            is_negative_test = contains_invalid_enum_value(
                request_schema, request_test_case
            )

        # Make the POST request
        try:
            response = make_request(
                "POST", url, json=request_test_case, timeout=timeout
            )
        except requests.exceptions.RequestException as e:
            error_msg = f"Request failed: {e}"
            log_test_result(
                "POST",
                path,
                request_test_case,
                expected_status,
                expected_response,
                None,
                None,
                False,
                error_msg,
                test_origin,
                documented_statuses=documented_statuses,
            )
            errors.append(error_msg)
            continue

        # If this is a negative test (invalid enum), expect 400
        if is_negative_test:
            # Parse response
            try:
                if response.text:
                    actual_response = response.json()
                else:
                    actual_response = ""
            except Exception:
                actual_response = response.text

            # Should get 400 Bad Request
            if response.status_code == 400:
                # Success - invalid enum was properly rejected
                log_test_result(
                    "POST",
                    path,
                    request_test_case,
                    400,
                    "400 Bad Request (invalid enum value)",
                    response.status_code,
                    actual_response,
                    True,
                    None,
                    test_origin,
                    documented_statuses=documented_statuses,
                )
                continue
            elif response.status_code >= 500:
                # Server error - this is bad, should have returned 400
                error_msg = f"Expected 400 for invalid enum value, got {response.status_code} (server error). Server should validate enum values and return 400, not 5xx."
                log_test_result(
                    "POST",
                    path,
                    request_test_case,
                    400,
                    "400 Bad Request (invalid enum value)",
                    response.status_code,
                    actual_response,
                    False,
                    error_msg,
                    test_origin,
                    documented_statuses=documented_statuses,
                )
                errors.append(error_msg)
                continue
            else:
                # Got 200/201 or other status
                # Invalid enum should have been rejected
                error_msg = (
                    f"Expected 400 for invalid enum value, got "
                    f"{response.status_code}. Server should validate "
                    f"enum values and return 400 Bad Request."
                )
                log_test_result(
                    "POST",
                    path,
                    request_test_case,
                    400,
                    "400 Bad Request (invalid enum value)",
                    response.status_code,
                    actual_response,
                    False,
                    error_msg,
                    test_origin,
                    documented_statuses=documented_statuses,
                )
                errors.append(error_msg)
                continue

        # Check status code (accept both 200 and 201 for POST)
        actual_response = (
            response.json()
            if response.status_code in [200, 201]
            else response.text
        )

        # In lenient mode, accept any documented status code
        if not strict_examples and response.status_code in documented_statuses:
            # Get the response schema/example for the actual status code
            actual_status_response = responses.get(
                str(response.status_code), {}
            )
            actual_content = actual_status_response.get("content", {})
            actual_expected_response = None
            actual_response_schema = None

            for media_type, media_obj in actual_content.items():
                if "example" in media_obj:
                    actual_expected_response = media_obj["example"]
                if "schema" in media_obj:
                    actual_response_schema = media_obj["schema"]
                break

            # Parse JSON response if possible
            try:
                if response.text:
                    actual_response = response.json()
            except Exception:
                pass

            # Validate against the actual status code's schema
            if actual_response_schema:
                matches, error = validate_against_schema(
                    actual_response_schema, actual_response
                )
            elif actual_expected_response:
                matches, error = compare_responses(
                    actual_expected_response, actual_response, strict=False
                )
            else:
                # No schema or example for this status, just accept it
                matches, error = True, None

            if matches:
                log_test_result(
                    "POST",
                    path,
                    request_test_case,
                    expected_status,
                    expected_response,
                    response.status_code,
                    actual_response,
                    True,
                    None,
                    "example",
                    documented_statuses=documented_statuses,
                )
                continue
            else:
                log_test_result(
                    "POST",
                    path,
                    request_test_case,
                    expected_status,
                    expected_response,
                    response.status_code,
                    actual_response,
                    False,
                    error,
                    test_origin,
                    documented_statuses=documented_statuses,
                )
                errors.append(error)
                continue

        # Accept 501 (Not Implemented) as valid if documented (for strict mode)
        if response.status_code == 501 and 501 in documented_statuses:
            log_test_result(
                "POST",
                path,
                request_test_case,
                expected_status,
                expected_response,
                response.status_code,
                actual_response,
                True,
                None,
                test_origin,
                documented_statuses=documented_statuses,
            )
            continue

        if response.status_code not in [200, 201]:
            error_msg = f"Expected status 200/201, got {response.status_code}. Response: {response.text}"
            log_test_result(
                "POST",
                path,
                request_test_case,
                expected_status,
                expected_response,
                response.status_code,
                actual_response,
                False,
                error_msg,
                test_origin,
                documented_statuses=documented_statuses,
            )
            errors.append(error_msg)
            continue

        # Check response matches example or schema
        # If request is example-based AND response has example, use strict/lenient matching
        # If request is schema-generated, always use schema validation for response
        if test_origin == "example" and response_is_example_based:
            matches, error = compare_responses(
                expected_response, actual_response, strict=strict_examples
            )
        elif response_schema:
            matches, error = validate_against_schema(
                response_schema, actual_response
            )
        else:
            matches, error = compare_responses(
                expected_response, actual_response, strict=True
            )

        if not matches:
            log_test_result(
                "POST",
                path,
                request_test_case,
                expected_status,
                expected_response,
                response.status_code,
                actual_response,
                False,
                error,
                test_origin,
                documented_statuses=documented_statuses,
            )
            errors.append(error)
            continue

        log_test_result(
            "POST",
            path,
            request_test_case,
            expected_status,
            expected_response,
            response.status_code,
            actual_response,
            True,
            None,
            test_origin,
            documented_statuses=documented_statuses,
        )

    if errors:
        # Return the first few errors for brevity
        combined = "; ".join(str(e) for e in errors[:3])
        return False, combined

    return True, None


def test_put_endpoint(
    base_url, path, operation, strict_examples=True, timeout=10
):
    """Test a PUT endpoint using the example from the OpenAPI spec.

    Args:
        base_url: Base URL of the API server
        path: API endpoint path (may contain path parameters)
        operation: OpenAPI operation object
        strict_examples: If True, strictly match example responses; if False, only validate structure

    Returns:
        tuple: (success: bool, error_message: str or None)
    """
    # For PUT endpoints with path parameters, only use example-based tests
    # Schema-generated tests don't work well because path params are extracted
    # from examples and the resource may not exist for generated test cases
    request_test_cases = []
    test_case_origins = (
        []
    )  # Track if each test case is 'example' or 'generated'
    warnings = []

    request_body = operation.get("requestBody", {})
    request_content = request_body.get("content", {})

    for media_type, media_obj in request_content.items():
        # Collect explicit examples
        if "example" in media_obj:
            request_test_cases.append(media_obj["example"])
            test_case_origins.append("example")
        if "examples" in media_obj:
            examples_dict = media_obj["examples"]
            for ex_name, ex_obj in examples_dict.items():
                if "value" in ex_obj:
                    request_test_cases.append(ex_obj["value"])
                    test_case_origins.append("example")

        # Skip schema-generated tests for PUT - they don't work well with path parameters
        # that reference specific resource IDs from examples
        break

    if not request_test_cases:
        return False, "No request body examples or schema found"

    # Print warnings if any
    for warning in warnings:
        print(f"\n{warning}")

    # Get the expected response from examples or generate from schema
    responses = operation.get("responses", {})
    response_200 = responses.get("200", {})
    content = response_200.get("content", {})

    # Get all documented response status codes
    documented_statuses = set()
    for status_code in responses.keys():
        try:
            documented_statuses.add(int(status_code))
        except (ValueError, TypeError):
            pass  # Skip non-numeric status codes like 'default'

    expected_response = None
    response_schema = None
    response_is_example_based = False

    for media_type, media_obj in content.items():
        if "example" in media_obj:
            expected_response = media_obj["example"]
            response_is_example_based = True
            # Also extract schema if present for schema-generated tests
            if "schema" in media_obj:
                response_schema = media_obj["schema"]
            break
        elif "examples" in media_obj:
            examples = media_obj["examples"]
            if examples:
                first_example = next(iter(examples.values()))
                expected_response = first_example.get("value")
                response_is_example_based = True
                # Also extract schema if present for schema-generated tests
                if "schema" in media_obj:
                    response_schema = media_obj["schema"]
                break

    # We are opinionated: examples are required
    if expected_response is None:
        return (
            False,
            "No example found for 200 response. Examples are required.",
        )

    # Replace path parameters with values from the response example
    url = f"{base_url}{path}"
    resolved_path = path
    if "{" in path:
        import re

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
            resolved_path = resolved_path.replace(
                f"{{{param_name}}}", str(value)
            )

    # Test all collected request cases
    errors = []
    for request_test_case, test_origin in zip(
        request_test_cases, test_case_origins
    ):
        # Check if this request contains an invalid enum value
        request_schema = None
        for media_type, media_obj in request_content.items():
            if "schema" in media_obj:
                request_schema = media_obj["schema"]
                break

        is_negative_test = False
        if request_schema:
            is_negative_test = contains_invalid_enum_value(
                request_schema, request_test_case
            )

        # Make the PUT request
        try:
            response = make_request(
                "PUT", url, json=request_test_case, timeout=timeout
            )
        except requests.exceptions.RequestException as e:
            error_msg = f"Request failed: {e}"
            log_test_result(
                "PUT",
                resolved_path,
                request_test_case,
                200,
                expected_response,
                None,
                None,
                False,
                error_msg,
                test_origin,
                documented_statuses=documented_statuses,
            )
            errors.append(error_msg)
            continue

        # If this is a negative test (invalid enum), expect 400
        if is_negative_test:
            # Parse response
            try:
                if response.text:
                    actual_response = response.json()
                else:
                    actual_response = ""
            except Exception:
                actual_response = response.text

            # Should get 400 Bad Request
            if response.status_code == 400:
                # Success - invalid enum was properly rejected
                log_test_result(
                    "PUT",
                    resolved_path,
                    request_test_case,
                    400,
                    "400 Bad Request (invalid enum value)",
                    response.status_code,
                    actual_response,
                    True,
                    None,
                    test_origin,
                    documented_statuses=documented_statuses,
                )
                continue
            elif response.status_code >= 500:
                # Server error - this is bad, should have returned 400
                error_msg = f"Expected 400 for invalid enum value, got {response.status_code} (server error). Server should validate enum values and return 400, not 5xx."
                log_test_result(
                    "PUT",
                    resolved_path,
                    request_test_case,
                    400,
                    "400 Bad Request (invalid enum value)",
                    response.status_code,
                    actual_response,
                    False,
                    error_msg,
                    test_origin,
                    documented_statuses=documented_statuses,
                )
                errors.append(error_msg)
                continue
            else:
                # Got 200 or other status - invalid enum should have been rejected
                error_msg = f"Expected 400 for invalid enum value, got {response.status_code}. Server should validate enum values and return 400 Bad Request."
                log_test_result(
                    "PUT",
                    resolved_path,
                    request_test_case,
                    400,
                    "400 Bad Request (invalid enum value)",
                    response.status_code,
                    actual_response,
                    False,
                    error_msg,
                    test_origin,
                    documented_statuses=documented_statuses,
                )
                errors.append(error_msg)
                continue

        # Check status code
        actual_response = (
            response.json() if response.status_code == 200 else response.text
        )

        # In lenient mode, accept any documented status code
        if not strict_examples and response.status_code in documented_statuses:
            # Get the response schema/example for the actual status code
            actual_status_response = responses.get(
                str(response.status_code), {}
            )
            actual_content = actual_status_response.get("content", {})
            actual_expected_response = None
            actual_response_schema = None

            for media_type, media_obj in actual_content.items():
                if "example" in media_obj:
                    actual_expected_response = media_obj["example"]
                if "schema" in media_obj:
                    actual_response_schema = media_obj["schema"]
                break

            # Parse JSON response if possible
            try:
                if response.text:
                    actual_response = response.json()
            except Exception:
                pass

            # Validate against the actual status code's schema
            if actual_response_schema:
                matches, error = validate_against_schema(
                    actual_response_schema, actual_response
                )
            elif actual_expected_response:
                matches, error = compare_responses(
                    actual_expected_response, actual_response, strict=False
                )
            else:
                # No schema or example for this status, just accept it
                matches, error = True, None

            if matches:
                log_test_result(
                    "PUT",
                    resolved_path,
                    request_test_case,
                    200,
                    expected_response,
                    response.status_code,
                    actual_response,
                    True,
                    None,
                    test_origin,
                    documented_statuses=documented_statuses,
                )
                continue
            else:
                log_test_result(
                    "PUT",
                    resolved_path,
                    request_test_case,
                    200,
                    expected_response,
                    response.status_code,
                    actual_response,
                    False,
                    error,
                    test_origin,
                    documented_statuses=documented_statuses,
                )
                errors.append(error)
                continue

        # Accept 501 (Not Implemented) as valid if documented (for strict mode)
        if response.status_code == 501 and 501 in documented_statuses:
            log_test_result(
                "PUT",
                resolved_path,
                request_test_case,
                200,
                expected_response,
                response.status_code,
                actual_response,
                True,
                None,
                test_origin,
                documented_statuses=documented_statuses,
            )
            continue

        if response.status_code != 200:
            error_msg = f"Expected status 200, got {response.status_code}. Response: {response.text}"
            log_test_result(
                "PUT",
                resolved_path,
                request_test_case,
                200,
                expected_response,
                response.status_code,
                actual_response,
                False,
                error_msg,
                test_origin,
                documented_statuses=documented_statuses,
            )
            errors.append(error_msg)
            continue

        # Check response matches example or schema
        # If request is example-based AND response has example, use strict/lenient matching
        # If request is schema-generated, always use schema validation for response
        if test_origin == "example" and response_is_example_based:
            matches, error = compare_responses(
                expected_response, actual_response, strict=strict_examples
            )
        elif response_schema:
            matches, error = validate_against_schema(
                response_schema, actual_response
            )
        else:
            matches, error = compare_responses(
                expected_response, actual_response, strict=True
            )

        if not matches:
            log_test_result(
                "PUT",
                resolved_path,
                request_test_case,
                200,
                expected_response,
                response.status_code,
                actual_response,
                False,
                error,
                test_origin,
                documented_statuses=documented_statuses,
            )
            errors.append(error)
            continue

        log_test_result(
            "PUT",
            resolved_path,
            request_test_case,
            200,
            expected_response,
            response.status_code,
            actual_response,
            True,
            None,
            test_origin,
            documented_statuses=documented_statuses,
        )

    if errors:
        combined = "; ".join(str(e) for e in errors[:3])
        return False, combined

    return True, None


def test_delete_endpoint(
    base_url, path, operation, strict_examples=True, timeout=10
):
    """Test a DELETE endpoint.

    Args:
        base_url: Base URL of the API server
        path: API endpoint path (may contain path parameters)
        operation: OpenAPI operation object
        strict_examples: If True, strictly match example responses; if False, only validate structure

    Returns:
        tuple: (success: bool, error_message: str or None)
    """
    # For DELETE, we need to get path parameters from the 200/204 response example or schema
    responses = operation.get("responses", {})

    # Get all documented response status codes
    documented_statuses = set()
    for status_code in responses.keys():
        try:
            documented_statuses.add(int(status_code))
        except (ValueError, TypeError):
            pass  # Skip non-numeric status codes like 'default'

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
            elif "examples" in media_obj:
                examples = media_obj["examples"]
                if examples:
                    first_example = next(iter(examples.values()))
                    response_example = first_example.get("value")
                    expected_body = response_example
                    break
            elif "schema" in media_obj:
                # Generate test cases from schema
                schema = media_obj["schema"]
                response_test_cases, warning = generate_test_cases_for_schema(
                    schema
                )
                if warning:
                    if isinstance(warning, list):
                        for w in warning:
                            print(f"\n{w}")
                    else:
                        print(f"\n{warning}")
                if response_test_cases:
                    response_example = response_test_cases[0]
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
            resolved_path = resolved_path.replace(
                f"{{{param_name}}}", str(param_value)
            )

    # Make the DELETE request
    try:
        response = make_request("DELETE", url, timeout=timeout)
    except requests.exceptions.RequestException as e:
        error_msg = f"Request failed: {e}"
        log_test_result(
            "DELETE",
            resolved_path,
            None,
            expected_status,
            expected_body,
            None,
            None,
            False,
            error_msg,
            "example",
            documented_statuses=documented_statuses,
        )
        return False, error_msg

    # Check status code (accept 200 or 204 for successful DELETE)
    actual_response = ""
    if response.status_code == 200 and response.text:
        try:
            actual_response = response.json()
        except Exception:
            actual_response = response.text

    # In lenient mode, accept any documented status code
    if not strict_examples and response.status_code in documented_statuses:
        # Get the response schema/example for the actual status code
        actual_status_response = responses.get(str(response.status_code), {})
        actual_content = actual_status_response.get("content", {})
        actual_expected_response = None
        actual_response_schema = None

        for media_type, media_obj in actual_content.items():
            if "example" in media_obj:
                actual_expected_response = media_obj["example"]
            if "schema" in media_obj:
                actual_response_schema = media_obj["schema"]
            break

        # Parse JSON response if possible
        try:
            if response.text:
                actual_response = response.json()
        except Exception:
            pass

        # Validate against the actual status code's schema
        if actual_response_schema:
            matches, error = validate_against_schema(
                actual_response_schema, actual_response
            )
        elif actual_expected_response:
            matches, error = compare_responses(
                actual_expected_response, actual_response, strict=False
            )
        else:
            # No schema or example for this status, just accept it
            matches, error = True, None

        if matches:
            log_test_result(
                "DELETE",
                resolved_path,
                None,
                expected_status,
                expected_body,
                response.status_code,
                actual_response,
                True,
                None,
                "example",
                documented_statuses=documented_statuses,
            )
            return True, None
        else:
            log_test_result(
                "DELETE",
                resolved_path,
                None,
                expected_status,
                expected_body,
                response.status_code,
                actual_response,
                False,
                error,
                "example",
                documented_statuses=documented_statuses,
            )
            return False, error

    # Accept 501 (Not Implemented) as valid if documented (for strict mode)
    if response.status_code == 501 and 501 in documented_statuses:
        log_test_result(
            "DELETE",
            resolved_path,
            None,
            expected_status,
            expected_body,
            response.status_code,
            actual_response,
            True,
            None,
            "example",
            documented_statuses=documented_statuses,
        )
        return True, None

    if response.status_code not in [200, 204]:
        error_msg = f"Expected status 200/204, got {response.status_code}. Response: {response.text}"
        log_test_result(
            "DELETE",
            resolved_path,
            None,
            expected_status,
            expected_body,
            response.status_code,
            actual_response,
            False,
            error_msg,
            "example",
            documented_statuses=documented_statuses,
        )
        return False, error_msg

    log_test_result(
        "DELETE",
        resolved_path,
        None,
        expected_status,
        expected_body,
        response.status_code,
        actual_response,
        True,
        None,
        "example",
        documented_statuses=documented_statuses,
    )
    return True, None
