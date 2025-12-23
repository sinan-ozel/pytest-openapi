"""Integration tests for pytest-openapi CLI functionality."""

import subprocess
import time
import pytest


def test_openapi_flag_is_recognized():
    """Test that --openapi flag is recognized by pytest (plugin is loaded)."""
    # Give the mock server time to start up
    time.sleep(2)

    # Run pytest with --openapi flag
    result = subprocess.run(
        ["pytest", "--openapi=http://mock-server-missing-openapi:8000", "-v"],
        capture_output=True,
        text=True,
        cwd="/app",
    )

    # Check that the flag is NOT unrecognized
    output = result.stdout + result.stderr
    assert "unrecognized arguments: --openapi" not in output, \
        f"Plugin not loaded: --openapi flag not recognized. Output: {output}"


@pytest.mark.depends(on=["test_openapi_flag_is_recognized"])
def test_missing_openapi_endpoint_fails():
    """Test that pytest --openapi fails when server lacks /openapi.json."""
    # Give the mock server time to start up
    time.sleep(2)

    # Run pytest with --openapi flag pointing to the mock server
    result = subprocess.run(
        ["pytest", "--openapi=http://mock-server-missing-openapi:8000", "-v"],
        capture_output=True,
        text=True,
        cwd="/app",
    )

    # Should fail because /openapi.json is not available
    assert result.returncode != 0, "Expected pytest to fail for missing OpenAPI endpoint"

    # Check that output indicates the failure
    output = result.stdout + result.stderr
    assert "openapi" in output.lower() or "error" in output.lower(), \
        f"Expected error message about OpenAPI in output, got: {output}"


@pytest.mark.depends(on=["test_openapi_flag_is_recognized"])
def test_missing_examples_fails():
    """Test that pytest --openapi fails when OpenAPI spec lacks examples."""
    # Give the mock server time to start up
    time.sleep(2)

    # Run pytest with --openapi flag pointing to the mock server
    result = subprocess.run(
        ["pytest", "--openapi=http://mock-server-no-examples:8000", "-v"],
        capture_output=True,
        text=True,
        cwd="/app",
    )

    # Should fail because OpenAPI spec has no examples
    assert result.returncode != 0, "Expected pytest to fail when examples are missing"

    # Check that output indicates the failure
    output = result.stdout + result.stderr
    assert "example" in output.lower() or "error" in output.lower(), \
        f"Expected error message about missing examples in output, got: {output}"


@pytest.mark.depends(on=["test_openapi_flag_is_recognized"])
def test_valid_api_passes():
    """Test that valid API with complete spec passes validation."""
    time.sleep(2)

    result = subprocess.run(
        ["pytest", "--openapi=http://mock-server-valid-api:8000", "-v"],
        capture_output=True,
        text=True,
        cwd="/app",
    )

    output = result.stdout + result.stderr
    assert "✅ OpenAPI spec validated successfully" in output, \
        f"Expected validation success, got: {output}"


@pytest.mark.depends(on=["test_openapi_flag_is_recognized"])
def test_get_missing_key_detected():
    """Test that GET response missing key is detected."""
    time.sleep(2)

    result = subprocess.run(
        ["pytest", "--openapi=http://mock-server-get-missing-key:8000", "-v"],
        capture_output=True,
        text=True,
        cwd="/app",
    )

    output = result.stdout + result.stderr
    assert "missing key" in output.lower() or "price" in output.lower(), \
        f"Expected error about missing key 'price', got: {output}"


@pytest.mark.depends(on=["test_openapi_flag_is_recognized"])
def test_get_type_mismatch_detected():
    """Test that GET response type mismatch is detected."""
    time.sleep(2)

    result = subprocess.run(
        ["pytest", "--openapi=http://mock-server-get-type-mismatch:8000", "-v"],
        capture_output=True,
        text=True,
        cwd="/app",
    )

    output = result.stdout + result.stderr
    assert "type mismatch" in output.lower() or ("str" in output.lower() and "int" in output.lower()), \
        f"Expected error about type mismatch, got: {output}"


@pytest.mark.depends(on=["test_openapi_flag_is_recognized"])
def test_post_500_error_detected():
    """Test that POST returning 500 instead of 200 is detected."""
    time.sleep(2)

    result = subprocess.run(
        ["pytest", "--openapi=http://mock-server-post-500-error:8000", "-v"],
        capture_output=True,
        text=True,
        cwd="/app",
    )

    output = result.stdout + result.stderr
    assert "500" in output, \
        f"Expected error mentioning status code 500, got: {output}"


@pytest.mark.depends(on=["test_openapi_flag_is_recognized"])
def test_post_response_missing_key_detected():
    """Test that POST response missing key is detected."""
    time.sleep(2)

    result = subprocess.run(
        ["pytest", "--openapi=http://mock-server-post-response-missing-key:8000", "-v"],
        capture_output=True,
        text=True,
        cwd="/app",
    )

    output = result.stdout + result.stderr
    assert "missing key" in output.lower() or "status" in output.lower(), \
        f"Expected error about missing key 'status', got: {output}"


@pytest.mark.depends(on=["test_openapi_flag_is_recognized"])
def test_post_example_missing_key_detected():
    """Test that POST response with extra key is detected."""
    time.sleep(2)

    result = subprocess.run(
        ["pytest", "--openapi=http://mock-server-post-example-missing-key:8000", "-v"],
        capture_output=True,
        text=True,
        cwd="/app",
    )

    output = result.stdout + result.stderr
    assert "extra key" in output.lower() or "created_at" in output.lower(), \
        f"Expected error about extra key 'created_at', got: {output}"


@pytest.mark.depends(on=["test_openapi_flag_is_recognized"])
def test_post_response_wrong_type_detected():
    """Test that POST response with wrong type is detected."""
    time.sleep(2)

    result = subprocess.run(
        ["pytest", "--openapi=http://mock-server-post-response-wrong-type:8000", "-v"],
        capture_output=True,
        text=True,
        cwd="/app",
    )

    output = result.stdout + result.stderr
    assert "type mismatch" in output.lower(), \
        f"Expected error about type mismatch, got: {output}"


@pytest.mark.depends(on=["test_openapi_flag_is_recognized"])
def test_put_response_missing_key_detected():
    """Test that PUT response missing key is detected."""
    time.sleep(2)

    result = subprocess.run(
        ["pytest", "--openapi=http://mock-server-put-response-missing-key:8000", "-v"],
        capture_output=True,
        text=True,
        cwd="/app",
    )

    output = result.stdout + result.stderr
    assert "missing key" in output.lower() or "updated" in output.lower(), \
        f"Expected error about missing key 'updated', got: {output}"


@pytest.mark.depends(on=["test_openapi_flag_is_recognized"])
def test_delete_wrong_status_detected():
    """Test that DELETE returning wrong status is detected."""
    time.sleep(2)

    result = subprocess.run(
        ["pytest", "--openapi=http://mock-server-delete-wrong-status:8000", "-v"],
        capture_output=True,
        text=True,
        cwd="/app",
    )

    output = result.stdout + result.stderr
    assert "500" in output, \
        f"Expected error mentioning status code 500, got: {output}"
