"""Integration tests for pytest-openapi CLI functionality."""

import subprocess
import time
import pytest
import sys


def test_openapi_flag_is_recognized():
    """Test that --openapi flag is recognized by pytest (plugin is loaded)."""
    print("\n🔍 Testing if --openapi flag is recognized...", flush=True)
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
    assert (
        "unrecognized arguments: --openapi" not in output
    ), f"Plugin not loaded: --openapi flag not recognized. Output: {output}"


@pytest.mark.depends(on=["test_openapi_flag_is_recognized"])
def test_missing_openapi_endpoint_fails():
    """Test that pytest --openapi fails when server lacks /openapi.json."""
    print("\n🔍 Testing missing OpenAPI endpoint detection...", flush=True)
    # Mock servers are already up from previous tests
    time.sleep(0.5)

    # Run pytest with --openapi flag pointing to the mock server
    result = subprocess.run(
        ["pytest", "--openapi=http://mock-server-missing-openapi:8000", "-v"],
        capture_output=True,
        text=True,
        cwd="/app",
    )

    # Should fail because /openapi.json is not available
    assert (
        result.returncode != 0
    ), "Expected pytest to fail for missing OpenAPI endpoint"

    # Check that output indicates the failure
    output = result.stdout + result.stderr
    assert (
        "openapi" in output.lower() or "error" in output.lower()
    ), f"Expected error message about OpenAPI in output, got: {output}"


@pytest.mark.depends(on=["test_openapi_flag_is_recognized"])
def test_missing_examples_fails():
    """Test that pytest --openapi fails when OpenAPI spec lacks examples."""
    print("\n🔍 Testing missing examples detection...", flush=True)
    time.sleep(0.5)

    # Run pytest with --openapi flag pointing to the mock server
    result = subprocess.run(
        ["pytest", "--openapi=http://mock-server-no-examples:8000", "-v"],
        capture_output=True,
        text=True,
        cwd="/app",
    )

    # Should fail because OpenAPI spec has no examples
    assert (
        result.returncode != 0
    ), "Expected pytest to fail when examples are missing"

    # Check that output indicates the failure
    output = result.stdout + result.stderr
    assert (
        "example" in output.lower() or "error" in output.lower()
    ), f"Expected error message about missing examples in output, got: {output}"


@pytest.mark.depends(on=["test_openapi_flag_is_recognized"])
def test_valid_api_passes():
    """Test that valid API with complete spec passes validation."""
    print("\n🔍 Testing valid API validation...", flush=True)
    time.sleep(0.5)

    result = subprocess.run(
        ["pytest", "--openapi=http://mock-server-valid-api:8000", "-v"],
        capture_output=True,
        text=True,
        cwd="/app",
    )

    output = result.stdout + result.stderr
    assert (
        "✅ OpenAPI spec validated successfully" in output
        or "✅ All contract tests passed!" in output
    ), f"Expected validation success, got: {output}"


@pytest.mark.depends(on=["test_openapi_flag_is_recognized"])
def test_get_missing_key_detected():
    """Test that GET response missing key is detected."""
    print("\n🔍 Testing GET missing key detection...", flush=True)
    time.sleep(0.5)

    result = subprocess.run(
        ["pytest", "--openapi=http://mock-server-get-missing-key:8000", "-v"],
        capture_output=True,
        text=True,
        cwd="/app",
    )

    output = result.stdout + result.stderr
    assert (
        "missing key" in output.lower() or "price" in output.lower()
    ), f"Expected error about missing key 'price', got: {output}"


@pytest.mark.depends(on=["test_openapi_flag_is_recognized"])
def test_get_type_mismatch_detected():
    """Test that GET response type mismatch is detected."""
    print("\n🔍 Testing GET type mismatch detection...", flush=True)
    time.sleep(0.5)

    result = subprocess.run(
        ["pytest", "--openapi=http://mock-server-get-type-mismatch:8000", "-v"],
        capture_output=True,
        text=True,
        cwd="/app",
    )

    output = result.stdout + result.stderr
    assert "type mismatch" in output.lower() or (
        "str" in output.lower() and "int" in output.lower()
    ), f"Expected error about type mismatch, got: {output}"


@pytest.mark.depends(on=["test_openapi_flag_is_recognized"])
def test_post_500_error_detected():
    """Test that POST returning 500 instead of 200 is detected."""
    print("\n🔍 Testing POST 500 error detection...", flush=True)
    time.sleep(0.5)

    result = subprocess.run(
        ["pytest", "--openapi=http://mock-server-post-500-error:8000", "-v"],
        capture_output=True,
        text=True,
        cwd="/app",
    )

    output = result.stdout + result.stderr
    assert (
        "500" in output
    ), f"Expected error mentioning status code 500, got: {output}"


@pytest.mark.depends(on=["test_openapi_flag_is_recognized"])
def test_post_response_missing_key_detected():
    """Test that POST response missing key is detected."""
    print("\n🔍 Testing POST response missing key detection...", flush=True)
    time.sleep(0.5)

    result = subprocess.run(
        [
            "pytest",
            "--openapi=http://mock-server-post-response-missing-key:8000",
            "-v",
        ],
        capture_output=True,
        text=True,
        cwd="/app",
    )

    output = result.stdout + result.stderr
    assert (
        "missing key" in output.lower() or "status" in output.lower()
    ), f"Expected error about missing key 'status', got: {output}"


@pytest.mark.depends(on=["test_openapi_flag_is_recognized"])
def test_post_example_missing_key_detected():
    """Test that POST response with extra key is detected."""
    print("\n🔍 Testing POST example extra key detection...", flush=True)
    time.sleep(0.5)

    result = subprocess.run(
        [
            "pytest",
            "--openapi=http://mock-server-post-example-missing-key:8000",
            "-v",
        ],
        capture_output=True,
        text=True,
        cwd="/app",
    )

    output = result.stdout + result.stderr
    assert (
        "extra key" in output.lower() or "created_at" in output.lower()
    ), f"Expected error about extra key 'created_at', got: {output}"


@pytest.mark.depends(on=["test_openapi_flag_is_recognized"])
def test_post_response_wrong_type_detected():
    """Test that POST response with wrong type is detected."""
    print("\n🔍 Testing POST response wrong type detection...", flush=True)
    time.sleep(0.5)

    result = subprocess.run(
        [
            "pytest",
            "--openapi=http://mock-server-post-response-wrong-type:8000",
            "-v",
        ],
        capture_output=True,
        text=True,
        cwd="/app",
    )

    output = result.stdout + result.stderr
    assert (
        "type mismatch" in output.lower()
    ), f"Expected error about type mismatch, got: {output}"


@pytest.mark.depends(on=["test_openapi_flag_is_recognized"])
def test_email_server_valid_and_invalid():
    """Test the email server: /email should pass, /email_bad should fail type checks."""
    print("\n🔍 Testing email server endpoints...", flush=True)
    time.sleep(0.5)

    # /email should validate successfully
    res_good = subprocess.run(
        [
            "pytest",
            "--openapi=http://mock-server-email-server:8000",
            "-k",
            "email and not bad",
            "-q",
        ],
        capture_output=True,
        text=True,
        cwd="/app",
    )
    out_good = res_good.stdout + res_good.stderr
    assert (
        "✅ OpenAPI spec validated successfully" in out_good
        or res_good.returncode == 0
    ), f"Expected /email to validate successfully, got: {out_good}"

    # /email_bad should fail due to type mismatch
    res_bad = subprocess.run(
        [
            "pytest",
            "--openapi=http://mock-server-email-server:8000",
            "-k",
            "email_bad",
            "-q",
        ],
        capture_output=True,
        text=True,
        cwd="/app",
    )
    out_bad = res_bad.stdout + res_bad.stderr
    assert (
        res_bad.returncode != 0
    ), f"Expected /email_bad tests to fail, got: {out_bad}"
    assert (
        "type mismatch" in out_bad.lower() or "expected str" in out_bad.lower()
    ), f"Expected type mismatch error for /email_bad, got: {out_bad}"


@pytest.mark.depends(on=["test_openapi_flag_is_recognized"])
def test_email_endpoint_passes():
    """Test that the /email endpoint validates successfully."""
    print("\n🔍 Testing /email validation...", flush=True)
    time.sleep(0.5)

    result = subprocess.run(
        [
            "pytest",
            "--openapi=http://mock-server-email-server:8000",
            "-k",
            "email and not bad",
            "-v",
        ],
        capture_output=True,
        text=True,
        cwd="/app",
    )

    output = result.stdout + result.stderr
    assert (
        "✅ OpenAPI spec validated successfully" in output
        or result.returncode == 0
    ), f"Expected /email to validate successfully, got: {output}"


@pytest.mark.depends(on=["test_openapi_flag_is_recognized"])
def test_email_bad_detected():
    """Test that /email_bad triggers a type-mismatch detection."""
    print("\n🔍 Testing /email_bad type-mismatch detection...", flush=True)
    time.sleep(0.5)

    result = subprocess.run(
        [
            "pytest",
            "--openapi=http://mock-server-email-server:8000",
            "-k",
            "email_bad",
            "-v",
        ],
        capture_output=True,
        text=True,
        cwd="/app",
    )

    output = result.stdout + result.stderr
    assert result.returncode != 0, f"Expected /email_bad to fail, got: {output}"
    assert (
        "type mismatch" in output.lower() or "expected str" in output.lower()
    ), f"Expected type mismatch error for /email_bad, got: {output}"


@pytest.mark.depends(on=["test_openapi_flag_is_recognized"])
def test_put_response_missing_key_detected():
    """Test that PUT response missing key is detected."""
    print("\n🔍 Testing PUT response missing key detection...", flush=True)
    time.sleep(0.5)

    result = subprocess.run(
        [
            "pytest",
            "--openapi=http://mock-server-put-response-missing-key:8000",
            "-v",
        ],
        capture_output=True,
        text=True,
        cwd="/app",
    )

    output = result.stdout + result.stderr
    assert (
        "missing key" in output.lower() or "updated" in output.lower()
    ), f"Expected error about missing key 'updated', got: {output}"


@pytest.mark.depends(on=["test_openapi_flag_is_recognized"])
def test_delete_wrong_status_detected():
    """Test that DELETE returning wrong status is detected."""
    print("\n🔍 Testing DELETE wrong status detection...", flush=True)
    time.sleep(0.5)

    result = subprocess.run(
        [
            "pytest",
            "--openapi=http://mock-server-delete-wrong-status:8000",
            "-v",
        ],
        capture_output=True,
        text=True,
        cwd="/app",
    )

    output = result.stdout + result.stderr
    assert (
        "500" in output
    ), f"Expected error mentioning status code 500, got: {output}"


@pytest.mark.depends(on=["test_openapi_flag_is_recognized"])
def test_schema_based_api_generates_examples():
    """Test that schema-based example generation works end-to-end."""
    print("\n🔍 Testing schema-based example generation...", flush=True)
    time.sleep(0.5)

    result = subprocess.run(
        ["pytest", "--openapi=http://mock-server-schema-based-api:8000", "-v"],
        capture_output=True,
        text=True,
        cwd="/app",
    )

    output = result.stdout + result.stderr

    # Should succeed - generated examples should work
    # Exit code is 0 because contract tests pass, then regular tests in /app are collected and pass
    assert (
        result.returncode == 0
    ), f"Expected schema-based API to pass with generated examples. Expected: exit code 0, got: {result.returncode}"

    # Check for validation success
    assert (
        "✅ OpenAPI spec validated successfully" in output
    ), f"Expected validation success, got: {output}"

    # Check that regular tests in /app were also collected and ran
    assert (
        "test_samples" in output and "3 passed" in output
    ), f"Expected regular tests to also run, got: {output}"

    # Count contract test entries (they are printed as 'Test #N')
    contract_tests = [
        line
        for line in output.splitlines()
        if line.strip().startswith("Test #")
    ]
    assert (
        len(contract_tests) >= 10
    ), f"Expected at least 10 contract tests, found {len(contract_tests)}\nOutput:\n{output}"
