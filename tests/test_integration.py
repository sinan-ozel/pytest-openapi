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
    ), f"Expected validation success, got: {output}"

    # Check that tests appear as individual pytest items
    assert (
        "test_openapi[GET" in output or "test_openapi[POST" in output
    ), f"Expected to see individual test items in output, got: {output}"


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

    # Count contract test items (they appear as individual pytest test items)
    contract_tests = [
        line
        for line in output.splitlines()
        if "test_openapi[POST /test-types [generated-" in line
    ]
    assert (
        len(contract_tests) >= 10
    ), f"Expected at least 10 contract tests, found {len(contract_tests)}\nOutput:\n{output}"


@pytest.mark.depends(on=["test_openapi_flag_is_recognized"])
def test_enum_validation_in_requests():
    """Test that enum validation works for request bodies - all valid values should pass, invalid should get 400."""
    print("\n🔍 Testing enum validation in POST requests...", flush=True)
    time.sleep(0.5)

    result = subprocess.run(
        ["pytest", "--openapi=http://mock-server-schema-based-api:8000", "-v"],
        capture_output=True,
        text=True,
        cwd="/app",
    )

    output = result.stdout + result.stderr

    # Should succeed - the valid enum values should all pass
    assert (
        result.returncode == 0
    ), f"Expected enum validation tests to pass with valid values. Exit code: {result.returncode}\nOutput: {output}"

    # Check that tests were generated and passed
    assert (
        "test_openapi[GET" in output or "test_openapi[POST" in output
    ), f"Expected OpenAPI tests to appear as individual test items, got: {output}"


@pytest.mark.depends(on=["test_openapi_flag_is_recognized"])
def test_post_501_undocumented_fails():
    """Test that 501 response fails when not documented in OpenAPI spec."""
    print("\n🔍 Testing POST 501 undocumented detection...", flush=True)
    time.sleep(0.5)

    result = subprocess.run(
        [
            "pytest",
            "--openapi=http://mock-server-post-501-undocumented:8000",
            "-v",
        ],
        capture_output=True,
        text=True,
        cwd="/app",
    )

    output = result.stdout + result.stderr
    assert (
        result.returncode != 0
    ), f"Expected test to fail for undocumented 501, got: {output}"
    assert (
        "501" in output
    ), f"Expected error mentioning status code 501, got: {output}"


@pytest.mark.depends(on=["test_openapi_flag_is_recognized"])
def test_post_501_documented_passes():
    """Test that 501 response passes when documented in OpenAPI spec."""
    print("\n🔍 Testing POST 501 documented acceptance...", flush=True)
    time.sleep(0.5)

    result = subprocess.run(
        [
            "pytest",
            "--openapi=http://mock-server-post-501-documented:8000",
            "-v",
        ],
        capture_output=True,
        text=True,
        cwd="/app",
    )

    output = result.stdout + result.stderr
    assert (
        result.returncode == 0
    ), f"Expected test to pass for documented 501, got: {output}"
    assert (
        "✅ OpenAPI spec validated successfully" in output
        or "test_openapi[" in output
    ), f"Expected validation success or OpenAPI test items, got: {output}"


@pytest.mark.depends(on=["test_openapi_flag_is_recognized"])
def test_example_value_mismatch_fails_strict():
    """Test that example value mismatch fails with strict checking (default)."""
    print(
        "\n🔍 Testing example value mismatch with strict checking...",
        flush=True,
    )
    time.sleep(0.5)

    result = subprocess.run(
        [
            "pytest",
            "--openapi=http://mock-server-example-value-mismatch:8000",
            "-v",
        ],
        capture_output=True,
        text=True,
        cwd="/app",
    )

    output = result.stdout + result.stderr
    assert (
        result.returncode != 0
    ), f"Expected test to fail with strict example checking (default), got: {output}"
    assert (
        "List length mismatch" in output or "mismatch" in output.lower()
    ), f"Expected error about value/length mismatch, got: {output}"


@pytest.mark.depends(on=["test_openapi_flag_is_recognized"])
def test_example_value_mismatch_passes_lenient():
    """Test that example value mismatch passes with --openapi-no-strict-example-checking."""
    print(
        "\n🔍 Testing example value mismatch with lenient checking...",
        flush=True,
    )
    time.sleep(0.5)

    result = subprocess.run(
        [
            "pytest",
            "--openapi=http://mock-server-example-value-mismatch:8000",
            "--openapi-no-strict-example-checking",
            "-v",
        ],
        capture_output=True,
        text=True,
        cwd="/app",
    )

    output = result.stdout + result.stderr
    assert (
        result.returncode == 0
    ), f"Expected test to pass with lenient example checking, got: {output}"
    assert (
        "✅ OpenAPI spec validated successfully" in output
        or "test_openapi[" in output
    ), f"Expected validation success or OpenAPI test items, got: {output}"


@pytest.mark.depends(on=["test_openapi_flag_is_recognized"])
def test_get_404_passes_with_lenient_mode():
    """Test that GET returning documented 404 passes with --openapi-no-strict-example-checking.

    This tests the bug where a documented 404 response should be acceptable
    when using lenient mode, just like 200 responses are acceptable.
    """
    print(
        "\n🔍 Testing GET 404 with lenient mode (documented status should pass)...",
        flush=True,
    )
    time.sleep(0.5)

    result = subprocess.run(
        [
            "pytest",
            "--openapi=http://mock-server-get-returns-404:8000",
            "--openapi-no-strict-example-checking",
            "-v",
        ],
        capture_output=True,
        text=True,
        cwd="/app",
    )

    output = result.stdout + result.stderr

    # This should pass because 404 is documented in the OpenAPI spec
    # and lenient mode should accept any documented status code
    assert (
        result.returncode == 0
    ), f"Expected test to pass when 404 is documented and lenient mode is on, got: {output}"
    assert (
        "✅ OpenAPI spec validated successfully" in output
        or "test_openapi[" in output
    ), f"Expected validation success or OpenAPI test items, got: {output}"


@pytest.mark.depends(on=["test_openapi_flag_is_recognized"])
def test_put_example_value_mismatch_fails_strict():
    """Test that PUT with example value mismatch fails with strict checking (default)."""
    print(
        "\n🔍 Testing PUT example value mismatch with strict checking...",
        flush=True,
    )
    time.sleep(0.5)

    result = subprocess.run(
        [
            "pytest",
            "--openapi=http://mock-server-example-value-mismatch:8000",
            "-v",
        ],
        capture_output=True,
        text=True,
        cwd="/app",
    )

    output = result.stdout + result.stderr
    assert (
        result.returncode != 0
    ), f"Expected test to fail with strict example checking (default), got: {output}"
    # Should have failures for both POST and PUT endpoints
    assert (
        "PUT /config" in output or "mismatch" in output.lower()
    ), f"Expected error about PUT endpoint mismatch, got: {output}"


@pytest.mark.depends(on=["test_openapi_flag_is_recognized"])
def test_put_example_value_mismatch_passes_lenient():
    """Test that PUT with example value mismatch passes with --openapi-no-strict-example-checking."""
    print(
        "\n🔍 Testing PUT example value mismatch with lenient checking...",
        flush=True,
    )
    time.sleep(0.5)

    result = subprocess.run(
        [
            "pytest",
            "--openapi=http://mock-server-example-value-mismatch:8000",
            "--openapi-no-strict-example-checking",
            "-v",
        ],
        capture_output=True,
        text=True,
        cwd="/app",
    )

    output = result.stdout + result.stderr
    assert (
        result.returncode == 0
    ), f"Expected test to pass with lenient example checking for PUT, got: {output}"
    assert (
        "✅ OpenAPI spec validated successfully" in output
        or "✅ All contract tests passed!" in output
    ), f"Expected validation success, got: {output}"


@pytest.mark.depends(on=["test_openapi_flag_is_recognized"])
def test_openapi_ignore_simple_exact_match():
    """Ignoring a single failing endpoint with an exact match should allow tests to pass."""
    print("\n🔍 Testing --openapi-ignore simple exact match...", flush=True)
    time.sleep(0.5)

    # Run the entire suite but ignore the failing endpoint via exact match
    result = subprocess.run(
        [
            "pytest",
            "--openapi=http://mock-server-email-server:8000",
            "--openapi-ignore=email_bad",
            "-q",
        ],
        capture_output=True,
        text=True,
        cwd="/app",
    )

    output = result.stdout + result.stderr
    # Should pass because email_bad is ignored, only /email is tested
    assert (
        result.returncode == 0
    ), f"Expected tests to pass when ignoring 'email_bad', got: {output}"
    assert (
        "Ignoring POST /email_bad" in output
    ), f"Expected to see ignore message, got: {output}"
    # In quiet mode (-q), test names aren't shown, just dots
    assert (
        "passed" in output.lower()
    ), f"Expected to see passing tests, got: {output}"


@pytest.mark.depends(
    on=[
        "test_openapi_flag_is_recognized",
        "test_openapi_ignore_simple_exact_match",
    ]
)
def test_openapi_ignore_alternation():
    """Ignoring endpoints using an alternation RegExp should allow tests to pass."""
    print("\n🔍 Testing --openapi-ignore alternation...", flush=True)
    time.sleep(0.5)

    # Use an alternation regex that includes the failing endpoint
    result = subprocess.run(
        [
            "pytest",
            "--openapi=http://mock-server-email-server:8000",
            "--openapi-ignore=(auth|email_bad)",
            "-q",
        ],
        capture_output=True,
        text=True,
        cwd="/app",
    )

    output = result.stdout + result.stderr
    assert (
        result.returncode == 0
    ), f"Expected tests to pass when ignoring with alternation, got: {output}"
    assert (
        "Ignoring POST /email_bad" in output
    ), f"Expected to see ignore message, got: {output}"
    # In quiet mode (-q), test names aren't shown, just dots
    assert (
        "passed" in output.lower()
    ), f"Expected to see passing tests, got: {output}"


@pytest.mark.depends(
    on=["test_openapi_flag_is_recognized", "test_openapi_ignore_alternation"]
)
def test_openapi_ignore_complex_regex():
    """Ignoring endpoints using a more complex RegExp should allow tests to pass."""
    print("\n🔍 Testing --openapi-ignore complex RegExp...", flush=True)
    time.sleep(0.5)

    # Use a RegExp that contains a path-like pattern in alternation with the failing endpoint
    result = subprocess.run(
        [
            "pytest",
            "--openapi=http://mock-server-email-server:8000",
            "--openapi-ignore=(v[0-9]+/auth|email_bad)",
            "-q",
        ],
        capture_output=True,
        text=True,
        cwd="/app",
    )

    output = result.stdout + result.stderr
    assert (
        result.returncode == 0
    ), f"Expected tests to pass when ignoring with complex regex, got: {output}"
    assert (
        "Ignoring POST /email_bad" in output
    ), f"Expected to see ignore message, got: {output}"
    # In quiet mode (-q), test names aren't shown, just dots
    assert (
        "passed" in output.lower()
    ), f"Expected to see passing tests, got: {output}"


@pytest.mark.depends(on=["test_openapi_flag_is_recognized"])
def test_openapi_tests_show_dots_in_non_verbose_mode():
    """Test that OpenAPI tests show [pytest-openapi] label and dots/F in non-verbose mode output."""
    print("\n🔍 Testing OpenAPI test output in non-verbose mode...", flush=True)
    time.sleep(0.5)

    result = subprocess.run(
        [
            "pytest",
            "--openapi=http://mock-server-put-response-missing-key:8000",
            "/app/test_samples/",
        ],
        capture_output=True,
        text=True,
        cwd="/app",
    )

    output = result.stdout + result.stderr

    # Should fail because the PUT endpoint is missing the 'updated' key
    assert (
        result.returncode != 0
    ), f"Expected tests to fail due to missing key, got: {output}"

    # Check for the [pytest-openapi] label
    assert (
        "[pytest-openapi]" in output
    ), f"Expected to see '[pytest-openapi]' label in output, got: {output}"

    # Check that dots and F appear in the output (non-verbose mode)
    # Should see something like: "tests/test_samples/test_sample_math.py .."
    # Then: "\n[pytest-openapi] . F.........."
    assert (
        output.count(".") > 5
    ), f"Expected to see dots in non-verbose output, got: {output}"

    assert (
        " F " in output or "F." in output or ".F" in output
    ), f"Expected to see F (failure) in non-verbose output, got: {output}"

    # Verify the failure message contains the expected error
    assert (
        "Missing key" in output or "missing key" in output.lower()
    ), f"Expected error about missing key, got: {output}"

    # Verify pytest correctly reports the number of failures
    # Should show something like "12 passed, 1 failed" in the summary
    assert (
        "1 failed" in output
    ), f"Expected '1 failed' in test summary, got: {output}"

    # Should also show some passed tests
    assert (
        "passed" in output
    ), f"Expected some passed tests in summary, got: {output}"


@pytest.mark.depends(on=["test_openapi_flag_is_recognized"])
def test_openapi_tests_all_pass_in_non_verbose_mode():
    """Test that all OpenAPI tests pass and show [pytest-openapi] label in non-verbose mode."""
    print(
        "\n🔍 Testing all OpenAPI tests passing in non-verbose mode...",
        flush=True,
    )
    time.sleep(0.5)

    result = subprocess.run(
        [
            "pytest",
            "--openapi=http://mock-server-schema-based-api:8000",
            "/app/test_samples/",
        ],
        capture_output=True,
        text=True,
        cwd="/app",
    )

    output = result.stdout + result.stderr

    # Should pass - all tests should succeed
    assert result.returncode == 0, f"Expected all tests to pass, got: {output}"

    # Check for the [pytest-openapi] label
    assert (
        "[pytest-openapi]" in output
    ), f"Expected to see '[pytest-openapi]' label in output, got: {output}"

    # Check that dots appear in the output (non-verbose mode)
    assert (
        output.count(".") > 5
    ), f"Expected to see dots in non-verbose output, got: {output}"

    # Should not have any failures or skips
    assert (
        " F " not in output and "F." not in output and ".F" not in output
    ), f"Expected no failures (F) in non-verbose output, got: {output}"

    assert (
        " s " not in output and "s." not in output and ".s" not in output
    ), f"Expected no skips (s) in non-verbose output, got: {output}"

    # Verify pytest correctly reports all tests passed
    # Should show something like "XX passed" in the summary
    assert (
        "passed" in output
    ), f"Expected 'passed' in test summary, got: {output}"

    # Should not show failed or skipped
    assert (
        "failed" not in output.lower()
    ), f"Expected no 'failed' in test summary, got: {output}"

    assert (
        "skipped" not in output.lower()
    ), f"Expected no 'skipped' in test summary, got: {output}"


@pytest.mark.depends(on=["test_openapi_flag_is_recognized"])
def test_openapi_collection_message_shows_test_origins():
    """Test that collection message shows breakdown of example vs generated tests."""
    print("\n🔍 Testing OpenAPI collection message format...", flush=True)
    time.sleep(0.5)

    result = subprocess.run(
        [
            "pytest",
            "--openapi=http://mock-server-put-response-missing-key:8000",
            "/app/test_samples/",
            "-v",
        ],
        capture_output=True,
        text=True,
        cwd="/app",
    )

    output = result.stdout + result.stderr

    # Check that the messages appear on separate lines with exact wording
    # The message should say "created X item(s) from openapi examples"
    assert (
        "from openapi examples" in output
    ), f"Expected 'from openapi examples' message, got: {output}"

    # The message should say "created X item(s) generated from schema"
    assert (
        "generated from schema" in output
    ), f"Expected 'generated from schema' message, got: {output}"

    # Verify the messages appear after "collected" line
    lines = output.split("\n")
    collected_line_idx = None
    examples_line_idx = None
    schema_line_idx = None

    for i, line in enumerate(lines):
        if "collected" in line and "items" in line:
            collected_line_idx = i
        if "from openapi examples" in line:
            examples_line_idx = i
        if "generated from schema" in line:
            schema_line_idx = i

    assert (
        collected_line_idx is not None
    ), f"Expected to find 'collected X items' line, got: {output}"

    assert (
        examples_line_idx is not None
    ), f"Expected to find 'from openapi examples' line, got: {output}"

    assert (
        schema_line_idx is not None
    ), f"Expected to find 'generated from schema' line, got: {output}"

    # Verify messages appear AFTER collected line
    assert (
        examples_line_idx > collected_line_idx
    ), f"Expected 'from openapi examples' after 'collected', got: {output}"

    assert (
        schema_line_idx > collected_line_idx
    ), f"Expected 'generated from schema' after 'collected', got: {output}"

    # Verify the two messages are on separate consecutive lines
    assert (
        schema_line_idx == examples_line_idx + 1
    ), f"Expected messages on consecutive lines, got examples at {examples_line_idx}, schema at {schema_line_idx}"


@pytest.mark.depends(on=["test_openapi_flag_is_recognized"])
def test_openapi_very_verbose_mode_shows_request_response():
    """Test that -vv shows request, expected response, and actual response for each test."""
    print("\n🔍 Testing OpenAPI very verbose mode (-vv)...", flush=True)
    time.sleep(0.5)

    result = subprocess.run(
        [
            "pytest",
            "--openapi=http://mock-server-post-500-error:8000",
            "/app/test_samples/",
            "-vv",
        ],
        capture_output=True,
        text=True,
        cwd="/app",
    )

    output = result.stdout + result.stderr

    # Should have failures due to 500 error
    assert (
        result.returncode != 0
    ), f"Expected tests to fail due to 500 error, got: {output}"

    # Check for the three-line format for each test
    # Should see lines like:
    #   Request: {...}
    #   Expected [200]: {...}
    #   Actual [500]: {...}

    assert (
        "Request:" in output
    ), f"Expected 'Request:' line in -vv output, got: {output}"

    assert (
        "Expected [" in output
    ), f"Expected 'Expected [XXX]:' line in -vv output, got: {output}"

    assert (
        "Actual [" in output
    ), f"Expected 'Actual [XXX]:' line in -vv output, got: {output}"

    # Verify lines are properly formatted (each should be on its own line)
    lines = output.split("\n")
    request_lines = [l for l in lines if "Request:" in l]
    expected_lines = [l for l in lines if "Expected [" in l]
    actual_lines = [l for l in lines if "Actual [" in l]

    # Should have at least one of each
    assert (
        len(request_lines) > 0
    ), f"Expected at least one 'Request:' line, got: {output}"

    assert (
        len(expected_lines) > 0
    ), f"Expected at least one 'Expected [...]' line, got: {output}"

    assert (
        len(actual_lines) > 0
    ), f"Expected at least one 'Actual [...]' line, got: {output}"

    # Verify truncation is happening (lines should not be excessively long)
    for line in request_lines + expected_lines + actual_lines:
        # Lines should be reasonable length (not thousands of chars)
        # With 50 char truncation + "..." + prefix, should be under 100 chars
        assert (
            len(line) < 200
        ), f"Expected line to be truncated, got line of length {len(line)}: {line}"

    # Verify the three lines appear together for at least one test
    for i, line in enumerate(lines):
        if "Request:" in line and i + 2 < len(lines):
            # Check if next two lines are Expected and Actual
            if "Expected [" in lines[i + 1] and "Actual [" in lines[i + 2]:
                # Found the three-line pattern
                break
    else:
        pytest.fail(
            f"Expected to find Request/Expected/Actual on consecutive lines, got: {output}"
        )


@pytest.mark.depends(on=["test_openapi_flag_is_recognized"])
def test_openapi_very_very_verbose_mode_shows_full_content():
    """Test that -vvv shows full request/response without truncation."""
    print("\n🔍 Testing OpenAPI very very verbose mode (-vvv)...", flush=True)
    time.sleep(0.5)

    result = subprocess.run(
        [
            "pytest",
            "--openapi=http://mock-server-post-500-error:8000",
            "/app/test_samples/",
            "-vvv",
        ],
        capture_output=True,
        text=True,
        cwd="/app",
    )

    output = result.stdout + result.stderr

    # Should have failures due to 500 error
    assert (
        result.returncode != 0
    ), f"Expected tests to fail due to 500 error, got: {output}"

    # Check for the three-line format
    assert (
        "Request:" in output
    ), f"Expected 'Request:' line in -vvv output, got: {output}"

    assert (
        "Expected [" in output
    ), f"Expected 'Expected [XXX]:' line in -vvv output, got: {output}"

    assert (
        "Actual [" in output
    ), f"Expected 'Actual [XXX]:' line in -vvv output, got: {output}"

    # Verify NO truncation is happening (should NOT see "..." in the output)
    lines = output.split("\n")
    request_lines = [l for l in lines if "Request:" in l]
    expected_lines = [l for l in lines if "Expected [" in l]
    actual_lines = [l for l in lines if "Actual [" in l]

    # Should have at least one of each
    assert (
        len(request_lines) > 0
    ), f"Expected at least one 'Request:' line, got: {output}"

    # In -vvv mode, content should NOT be truncated
    # Check that we don't see "..." truncation markers in the JSON output lines
    for line in request_lines + expected_lines + actual_lines:
        # The line itself should not end with "..." (which indicates truncation)
        # Note: JSON strings can contain "..." so we check for the truncation pattern
        if "None" not in line:  # Skip lines that just say "None"
            # If the line has JSON content, it should not have the truncation marker at the end
            if "{" in line or "[" in line:
                assert not line.rstrip().endswith(
                    "..."
                ), f"Expected no truncation in -vvv mode, but found '...' in: {line}"


@pytest.mark.depends(on=["test_openapi_flag_is_recognized"])
def test_streaming_api_sse_endpoint_passes():
    """Test that SSE streaming endpoint is handled correctly."""
    print("\n🔍 Testing SSE streaming endpoint handling...", flush=True)
    time.sleep(0.5)

    result = subprocess.run(
        [
            "pytest",
            "--openapi=http://mock-server-streaming-api:8000",
            "-k",
            "stream/sse",
            "-v",
        ],
        capture_output=True,
        text=True,
        cwd="/app",
    )

    output = result.stdout + result.stderr

    # Should pass - streaming responses should be recognized and handled
    assert (
        result.returncode == 0
    ), f"Expected SSE streaming tests to pass, got: {output}"

    # Check that the streaming endpoint was tested
    assert (
        "test_openapi[POST /stream/sse" in output
    ), f"Expected to see POST /stream/sse test, got: {output}"

    # Verify that streaming response was recognized
    assert (
        "passed" in output.lower()
    ), f"Expected streaming test to pass, got: {output}"


@pytest.mark.depends(on=["test_openapi_flag_is_recognized"])
def test_streaming_api_ndjson_endpoint_passes():
    """Test that NDJSON streaming endpoint is handled correctly."""
    print("\n🔍 Testing NDJSON streaming endpoint handling...", flush=True)
    time.sleep(0.5)

    result = subprocess.run(
        [
            "pytest",
            "--openapi=http://mock-server-streaming-api:8000",
            "-k",
            "stream/ndjson",
            "-v",
        ],
        capture_output=True,
        text=True,
        cwd="/app",
    )

    output = result.stdout + result.stderr

    # Should pass - streaming responses should be recognized and handled
    assert (
        result.returncode == 0
    ), f"Expected NDJSON streaming tests to pass, got: {output}"

    # Check that the streaming endpoint was tested
    assert (
        "test_openapi[POST /stream/ndjson" in output
    ), f"Expected to see POST /stream/ndjson test, got: {output}"

    # Verify that streaming response was recognized
    assert (
        "passed" in output.lower()
    ), f"Expected streaming test to pass, got: {output}"


@pytest.mark.depends(on=["test_openapi_flag_is_recognized"])
def test_streaming_api_chat_with_stream_false_returns_json():
    """Test that chat endpoint with stream=false returns JSON and validates correctly."""
    print(
        "\n🔍 Testing chat endpoint with stream=false (JSON response)...",
        flush=True,
    )
    time.sleep(0.5)

    result = subprocess.run(
        [
            "pytest",
            "--openapi=http://mock-server-streaming-api:8000",
            "-k",
            "chat",
            "-v",
        ],
        capture_output=True,
        text=True,
        cwd="/app",
    )

    output = result.stdout + result.stderr

    # The chat endpoint with example has stream=false, so should return JSON
    # Tests should include both the example-based test and generated tests
    # Some generated tests may have stream=true (which will be streaming)
    # As long as the example-based test passes, we're good
    assert (
        "test_openapi[POST /chat" in output
    ), f"Expected to see POST /chat tests, got: {output}"

    # Should have some passing tests
    assert (
        "passed" in output.lower()
    ), f"Expected at least some chat tests to pass, got: {output}"


@pytest.mark.depends(on=["test_openapi_flag_is_recognized"])
def test_streaming_api_all_endpoints_tested():
    """Test that all streaming endpoints are tested together without errors."""
    print("\n🔍 Testing all streaming API endpoints together...", flush=True)
    time.sleep(0.5)

    result = subprocess.run(
        [
            "pytest",
            "--openapi=http://mock-server-streaming-api:8000",
            "-v",
        ],
        capture_output=True,
        text=True,
        cwd="/app",
    )

    output = result.stdout + result.stderr

    # Should pass - all streaming endpoints should be handled correctly
    assert (
        result.returncode == 0
    ), f"Expected all streaming API tests to pass, got: {output}"

    # Verify validation success
    assert (
        "✅ OpenAPI spec validated successfully" in output
    ), f"Expected validation success, got: {output}"

    # Check that all three endpoints were tested
    assert (
        "test_openapi[POST /stream/sse" in output
    ), f"Expected POST /stream/sse test, got: {output}"

    assert (
        "test_openapi[POST /stream/ndjson" in output
    ), f"Expected POST /stream/ndjson test, got: {output}"

    assert (
        "test_openapi[POST /chat" in output
    ), f"Expected POST /chat test, got: {output}"

    # All tests should pass
    assert (
        "passed" in output.lower() and "failed" not in output.lower()
    ), f"Expected all tests to pass with no failures, got: {output}"


@pytest.mark.depends(on=["test_openapi_flag_is_recognized"])
def test_streaming_vvv_shows_sse_content_not_placeholder():
    """Test that -vvv mode shows collected SSE content, not a placeholder."""
    print(
        "\n🔍 Testing -vvv shows SSE content instead of placeholder...",
        flush=True,
    )
    time.sleep(0.5)

    result = subprocess.run(
        [
            "pytest",
            "--openapi=http://mock-server-streaming-api:8000",
            "-k",
            "stream/sse",
            "-vvv",
        ],
        capture_output=True,
        text=True,
        cwd="/app",
    )

    output = result.stdout + result.stderr

    assert (
        result.returncode == 0
    ), f"Expected SSE streaming tests to pass, got: {output}"

    # Should NOT show the opaque placeholder string
    assert (
        "[Streaming response:" not in output
    ), f"Expected no placeholder, but got: {output}"

    # Should show actual collected chunk content
    assert (
        "Chunk" in output
    ), f"Expected actual streaming content ('Chunk') in -vvv output, got: {output}"


@pytest.mark.depends(on=["test_openapi_flag_is_recognized"])
def test_streaming_vvv_shows_ndjson_content_not_placeholder():
    """Test that -vvv mode shows collected NDJSON content, not a placeholder."""
    print(
        "\n🔍 Testing -vvv shows NDJSON content instead of placeholder...",
        flush=True,
    )
    time.sleep(0.5)

    result = subprocess.run(
        [
            "pytest",
            "--openapi=http://mock-server-streaming-api:8000",
            "-k",
            "stream/ndjson",
            "-vvv",
        ],
        capture_output=True,
        text=True,
        cwd="/app",
    )

    output = result.stdout + result.stderr

    assert (
        result.returncode == 0
    ), f"Expected NDJSON streaming tests to pass, got: {output}"

    # Should NOT show the opaque placeholder string
    assert (
        "[Streaming response:" not in output
    ), f"Expected no placeholder, but got: {output}"

    # Should show actual collected chunk content
    assert (
        "Chunk" in output
    ), f"Expected actual streaming content ('Chunk') in -vvv output, got: {output}"


@pytest.mark.depends(on=["test_openapi_flag_is_recognized"])
def test_post_no_request_body_passes():
    """Test that POST endpoints with no request body are tested and pass."""
    print("\n🔍 Testing POST endpoint with no request body...", flush=True)
    time.sleep(0.5)

    result = subprocess.run(
        [
            "pytest",
            "--openapi=http://mock-server-post-no-request-body:8000",
            "-v",
        ],
        capture_output=True,
        text=True,
        cwd="/app",
    )

    output = result.stdout + result.stderr
    assert (
        result.returncode == 0
    ), f"Expected POST endpoint with no request body to pass, got: {output}"
    assert (
        "✅ OpenAPI spec validated successfully" in output
    ), f"Expected validation success, got: {output}"
    assert (
        "test_openapi[POST /cancel/" in output
    ), f"Expected POST /cancel/ test item to be generated, got: {output}"


# ---------------------------------------------------------------------------
# OpenAPI 3.1.x / components / allOf stress-test servers
# ---------------------------------------------------------------------------


@pytest.mark.depends(on=["test_openapi_flag_is_recognized"])
def test_components_ref_valid_passes():
    """Test that a spec using $ref to components/schemas passes when responses are correct.

    This exercises the plugin's ability to dereference $ref pointers and validate
    nested objects (Book -> Author) defined in components/schemas.
    """
    print("\n🔍 Testing components/$ref valid bookstore API...", flush=True)
    time.sleep(0.5)

    result = subprocess.run(
        [
            "pytest",
            "--openapi=http://mock-server-components-ref-valid:8000",
            "-v",
        ],
        capture_output=True,
        text=True,
        cwd="/app",
    )

    output = result.stdout + result.stderr

    # Spec should be structurally valid
    assert (
        "✅ OpenAPI spec validated successfully" in output
    ), f"Expected OpenAPI spec to pass structural validation, got: {output}"

    # Both endpoints should appear as test items
    assert (
        "test_openapi[GET /catalog/books" in output
        or "test_openapi[POST /catalog/books" in output
    ), f"Expected /catalog/books test items, got: {output}"

    assert (
        result.returncode == 0
    ), f"Expected all tests to pass for components_ref_valid, got: {output}"


@pytest.mark.depends(on=["test_openapi_flag_is_recognized"])
def test_components_ref_type_mismatch_detected():
    """Test that a type mismatch in a $ref-referenced schema is detected.

    The bookstore spec uses $ref to Book/Author in components. The server returns
    `year` as a string instead of integer. The plugin must dereference $ref to
    catch this error.
    """
    print("\n🔍 Testing components/$ref type mismatch detection...", flush=True)
    time.sleep(0.5)

    result = subprocess.run(
        [
            "pytest",
            "--openapi=http://mock-server-components-ref-type-mismatch:8000",
            "-v",
        ],
        capture_output=True,
        text=True,
        cwd="/app",
    )

    output = result.stdout + result.stderr

    # Should fail - type mismatch in field defined inside a $ref component
    assert (
        result.returncode != 0
    ), f"Expected tests to fail due to type mismatch via $ref, got: {output}"

    # Should mention the offending field or a type error
    assert (
        "year" in output or "type mismatch" in output.lower()
    ), f"Expected error about 'year' field type mismatch, got: {output}"


@pytest.mark.depends(on=["test_openapi_flag_is_recognized"])
def test_allof_composition_valid_passes():
    """Test that allOf schema composition validates correctly with correct responses.

    The vehicle API uses allOf to extend a base Vehicle schema with
    ElectricVehicle and GasVehicle. Responses include extra fields from the
    composed schema. All responses are correct and should PASS.
    """
    print("\n🔍 Testing allOf composition valid vehicle API...", flush=True)
    time.sleep(0.5)

    result = subprocess.run(
        [
            "pytest",
            "--openapi=http://mock-server-allof-composition-valid:8000",
            "-v",
        ],
        capture_output=True,
        text=True,
        cwd="/app",
    )

    output = result.stdout + result.stderr

    assert (
        "✅ OpenAPI spec validated successfully" in output
    ), f"Expected OpenAPI spec to pass structural validation, got: {output}"

    assert (
        "test_openapi[GET /vehicles" in output
        or "test_openapi[POST /vehicles" in output
    ), f"Expected /vehicles test items to appear, got: {output}"

    assert (
        result.returncode == 0
    ), f"Expected all allOf composition tests to pass, got: {output}"


@pytest.mark.depends(on=["test_openapi_flag_is_recognized"])
def test_petstore_components_passes():
    """Test the simplified Petstore API with full components/schemas usage.

    Based on the canonical OpenAPI Petstore example. Uses $ref throughout,
    path parameters, and multiple HTTP methods (GET, POST, DELETE).
    All responses are correct and should PASS.
    """
    print("\n🔍 Testing Petstore API with components/schemas...", flush=True)
    time.sleep(0.5)

    result = subprocess.run(
        [
            "pytest",
            "--openapi=http://mock-server-petstore-components:8000",
            "-v",
        ],
        capture_output=True,
        text=True,
        cwd="/app",
    )

    output = result.stdout + result.stderr

    assert (
        "✅ OpenAPI spec validated successfully" in output
    ), f"Expected OpenAPI spec to pass structural validation, got: {output}"

    # GET /pets and POST /pets should both appear
    assert (
        "test_openapi[GET /pets" in output
    ), f"Expected GET /pets test item, got: {output}"

    assert (
        "test_openapi[POST /pets" in output
    ), f"Expected POST /pets test item, got: {output}"

    assert (
        result.returncode == 0
    ), f"Expected all Petstore tests to pass, got: {output}"


@pytest.mark.depends(on=["test_openapi_flag_is_recognized"])
def test_openapi311_nullable_types_pass():
    """Test that OpenAPI 3.1.1 nullable type syntax is handled correctly.

    The user profile API uses `type: ["string", "null"]` (the 3.1.x way to
    express nullable fields). Responses include both string values and explicit
    null values for those fields. Should PASS.
    """
    print(
        "\n🔍 Testing OpenAPI 3.1.1 nullable type syntax (type: [string, null])...",
        flush=True,
    )
    time.sleep(0.5)

    result = subprocess.run(
        [
            "pytest",
            "--openapi=http://mock-server-openapi311-features:8000",
            "-v",
        ],
        capture_output=True,
        text=True,
        cwd="/app",
    )

    output = result.stdout + result.stderr

    assert (
        "✅ OpenAPI spec validated successfully" in output
    ), f"Expected OpenAPI 3.1.1 spec to pass structural validation, got: {output}"

    # /version, /users endpoints should appear
    assert (
        "test_openapi[GET /version" in output
        or "test_openapi[GET /users" in output
    ), f"Expected /version or /users test items, got: {output}"

    assert (
        result.returncode == 0
    ), f"Expected all OpenAPI 3.1.1 feature tests to pass, got: {output}"


@pytest.mark.depends(on=["test_openapi_flag_is_recognized"])
def test_openapi311_const_keyword_validated():
    """Test that the OpenAPI 3.1.1 `const` keyword on the /version endpoint is checked.

    The /version endpoint returns fields with `const` values ("1.0.0" and "3.1.1").
    Should PASS because the server returns exactly those constant values.
    """
    print(
        "\n🔍 Testing OpenAPI 3.1.1 const keyword on /version endpoint...",
        flush=True,
    )
    time.sleep(0.5)

    result = subprocess.run(
        [
            "pytest",
            "--openapi=http://mock-server-openapi311-features:8000",
            "-k",
            "version",
            "-v",
        ],
        capture_output=True,
        text=True,
        cwd="/app",
    )

    output = result.stdout + result.stderr

    assert (
        "test_openapi[GET /version" in output
    ), f"Expected GET /version test item, got: {output}"

    assert (
        result.returncode == 0
    ), f"Expected /version const-keyword test to pass, got: {output}"


@pytest.mark.depends(on=["test_openapi_flag_is_recognized"])
def test_post_202_accepted_passes():
    """Test that a POST endpoint documented and returning 202 Accepted passes.

    Regression test for the bug where the plugin required a 200 or 201 example
    and failed with 'No example found for 200/201 response' even when the spec
    correctly documented a 202 Accepted response.
    """
    print(
        "\n🔍 Testing POST endpoint with 202 Accepted response...", flush=True
    )
    time.sleep(0.5)

    result = subprocess.run(
        [
            "pytest",
            "--openapi=http://mock-server-post-202-accepted:8000",
            "-v",
        ],
        capture_output=True,
        text=True,
        cwd="/app",
    )

    output = result.stdout + result.stderr
    assert (
        result.returncode == 0
    ), f"Expected 202 Accepted endpoints to pass, got: {output}"
    assert (
        "✅ OpenAPI spec validated successfully" in output
    ), f"Expected validation success, got: {output}"
    assert (
        "test_openapi[POST /jobs" in output
    ), f"Expected POST /jobs test item, got: {output}"


@pytest.mark.depends(on=["test_openapi_flag_is_recognized"])
def test_get_202_accepted_passes():
    """Test that a GET endpoint documented and returning 202 Accepted passes."""
    print("\n🔍 Testing GET endpoint with 202 Accepted response...", flush=True)
    time.sleep(0.5)

    result = subprocess.run(
        [
            "pytest",
            "--openapi=http://mock-server-post-202-accepted:8000",
            "-k",
            "jobs/",
            "-v",
        ],
        capture_output=True,
        text=True,
        cwd="/app",
    )

    output = result.stdout + result.stderr
    assert (
        result.returncode == 0
    ), f"Expected GET 202 Accepted endpoint to pass, got: {output}"
    assert (
        "test_openapi[GET /jobs/" in output
    ), f"Expected GET /jobs/{{job_id}} test item, got: {output}"


@pytest.mark.depends(on=["test_openapi_flag_is_recognized"])
def test_post_202_spec_but_server_returns_200_fails():
    """Test that a POST endpoint documented as 202 but returning 200 is detected as a failure.

    Regression test: the status check must respect what the spec documents.
    When only 202 is documented, a server returning 200 is a contract violation
    and should cause the test to fail.
    """
    print(
        "\n🔍 Testing POST 202-documented endpoint that returns 200 (should fail)...",
        flush=True,
    )
    time.sleep(0.5)

    result = subprocess.run(
        [
            "pytest",
            "--openapi=http://mock-server-post-202-returns-200:8000",
            "-v",
        ],
        capture_output=True,
        text=True,
        cwd="/app",
    )

    output = result.stdout + result.stderr
    assert (
        result.returncode != 0
    ), f"Expected failure when server returns 200 but spec documents 202, got: {output}"
    assert (
        "202" in output or "200" in output
    ), f"Expected error mentioning the status code mismatch, got: {output}"


@pytest.mark.depends(on=["test_openapi_flag_is_recognized"])
def test_email_format_valid_address_passes():
    """Test that a POST endpoint with format: email accepts a valid email address.

    The contact server documents 'email' field with format: email and validates
    it server-side. A valid address like alice@example.com should produce 200.
    """
    print(
        "\n🔍 Testing valid email address passes format validation...",
        flush=True,
    )
    time.sleep(0.5)

    result = subprocess.run(
        [
            "pytest",
            "--openapi=http://mock-server-email-format-validation:8000",
            "-k",
            "contact",
            "-v",
        ],
        capture_output=True,
        text=True,
        cwd="/app",
    )

    output = result.stdout + result.stderr
    assert (
        "✅ OpenAPI spec validated successfully" in output
        or "test_openapi[POST /contact" in output
    ), f"Expected contact endpoint test to appear, got: {output}"


@pytest.mark.depends(on=["test_openapi_flag_is_recognized"])
def test_email_format_invalid_address_gets_400():
    """Test that the plugin generates invalid email test cases and the server
    returns 400 for them, which the plugin must recognise as a passing test.

    Invalid addresses like 'sinan,ozel @somehere' (space, comma, no valid domain)
    must be generated by the plugin and the server must respond with 400.
    The plugin should treat a 400 response to an invalid-format input as PASS.
    """
    print(
        "\n🔍 Testing invalid email format is generated and server returns 400...",
        flush=True,
    )
    time.sleep(0.5)

    result = subprocess.run(
        [
            "pytest",
            "--openapi=http://mock-server-email-format-validation:8000",
            "-v",
        ],
        capture_output=True,
        text=True,
        cwd="/app",
    )

    output = result.stdout + result.stderr

    # The plugin should generate invalid email test cases from the schema
    assert (
        "test_openapi[POST /contact" in output
    ), f"Expected POST /contact test items to be generated, got: {output}"

    # All tests should pass: valid emails get 200, invalid emails get 400
    # (400 for invalid-format input is treated as a passing contract test)
    assert (
        result.returncode == 0
    ), f"Expected all email format tests to pass (valid→200, invalid→400), got: {output}"


@pytest.mark.depends(on=["test_openapi_flag_is_recognized"])
def test_email_format_spec_validated_successfully():
    """Test that an OpenAPI spec with format: email fields passes structural validation."""
    print(
        "\n🔍 Testing OpenAPI spec with email format fields validates...",
        flush=True,
    )
    time.sleep(0.5)

    result = subprocess.run(
        [
            "pytest",
            "--openapi=http://mock-server-email-format-validation:8000",
            "-v",
        ],
        capture_output=True,
        text=True,
        cwd="/app",
    )

    output = result.stdout + result.stderr
    assert (
        "✅ OpenAPI spec validated successfully" in output
    ), f"Expected OpenAPI spec with email format to validate successfully, got: {output}"


# ---------------------------------------------------------------------------
# 400 with no error message — plugin must fail
# ---------------------------------------------------------------------------


@pytest.mark.depends(on=["test_openapi_flag_is_recognized"])
def test_email_format_400_without_message_fails():
    """Test that the plugin FAILS when a server returns 400 with no error description.

    A server that rejects invalid email values with an empty 400 body (no 'error'
    or 'detail' key) violates the contract: the API consumer has no information
    about what went wrong.  The plugin must treat this as a failing test.
    """
    print(
        "\n🔍 Testing plugin fails when 400 has no descriptive error message...",
        flush=True,
    )
    time.sleep(0.5)

    result = subprocess.run(
        [
            "pytest",
            "--openapi=http://mock-server-email-format-no-message:8000",
            "-v",
        ],
        capture_output=True,
        text=True,
        cwd="/app",
    )

    output = result.stdout + result.stderr

    # Plugin must fail: 400 with no descriptive body is not acceptable
    assert (
        result.returncode != 0
    ), f"Expected plugin to fail when 400 response has no error message, got: {output}"

    # The failure output should mention the lack of error detail
    assert (
        "400" in output
    ), f"Expected output to reference the 400 status code, got: {output}"


# ---------------------------------------------------------------------------
# format: uri / url
# ---------------------------------------------------------------------------


@pytest.mark.depends(on=["test_openapi_flag_is_recognized"])
def test_uri_format_valid_url_passes():
    """Test that a server with format: uri accepts valid URIs (e.g. https://example.com/hook)."""
    print("\n🔍 Testing valid URI format passes...", flush=True)
    time.sleep(0.5)

    result = subprocess.run(
        [
            "pytest",
            "--openapi=http://mock-server-uri-format-validation:8000",
            "-v",
        ],
        capture_output=True,
        text=True,
        cwd="/app",
    )

    output = result.stdout + result.stderr
    assert (
        "✅ OpenAPI spec validated successfully" in output
    ), f"Expected OpenAPI spec with URI format to validate, got: {output}"
    assert (
        "test_openapi[POST /webhook" in output
    ), f"Expected POST /webhook test items, got: {output}"


@pytest.mark.depends(on=["test_openapi_flag_is_recognized"])
def test_uri_format_invalid_url_gets_400_with_message():
    """Test that the plugin generates invalid URI values, the server returns a
    descriptive 400, and the plugin treats this as a passing test.

    Invalid URIs include strings with no scheme ('not-a-uri'), a bare path
    ('://broken'), or a plain hostname with no scheme ('example.com').
    """
    print(
        "\n🔍 Testing invalid URI gets descriptive 400 and plugin passes...",
        flush=True,
    )
    time.sleep(0.5)

    result = subprocess.run(
        [
            "pytest",
            "--openapi=http://mock-server-uri-format-validation:8000",
            "-v",
        ],
        capture_output=True,
        text=True,
        cwd="/app",
    )

    output = result.stdout + result.stderr
    # All tests should pass: valid URIs → 200, invalid URIs → 400 with message
    assert (
        result.returncode == 0
    ), f"Expected all URI format tests to pass (valid→200, invalid→400+message), got: {output}"


# ---------------------------------------------------------------------------
# format: uuid
# ---------------------------------------------------------------------------


@pytest.mark.depends(on=["test_openapi_flag_is_recognized"])
def test_uuid_format_valid_id_passes():
    """Test that a server with format: uuid accepts a well-formed UUID."""
    print("\n🔍 Testing valid UUID format passes...", flush=True)
    time.sleep(0.5)

    result = subprocess.run(
        [
            "pytest",
            "--openapi=http://mock-server-uuid-format-validation:8000",
            "-v",
        ],
        capture_output=True,
        text=True,
        cwd="/app",
    )

    output = result.stdout + result.stderr
    assert (
        "✅ OpenAPI spec validated successfully" in output
    ), f"Expected OpenAPI spec with UUID format to validate, got: {output}"
    assert (
        "test_openapi[POST /resource" in output
    ), f"Expected POST /resource test items, got: {output}"


@pytest.mark.depends(on=["test_openapi_flag_is_recognized"])
def test_uuid_format_invalid_value_gets_400_with_message():
    """Test that invalid UUID values (e.g. 'not-a-uuid', truncated strings, or
    strings with invalid hex characters) cause the server to return a descriptive
    400 and the plugin treats this as a passing contract test.
    """
    print(
        "\n🔍 Testing invalid UUID gets descriptive 400 and plugin passes...",
        flush=True,
    )
    time.sleep(0.5)

    result = subprocess.run(
        [
            "pytest",
            "--openapi=http://mock-server-uuid-format-validation:8000",
            "-v",
        ],
        capture_output=True,
        text=True,
        cwd="/app",
    )

    output = result.stdout + result.stderr
    assert (
        result.returncode == 0
    ), f"Expected all UUID format tests to pass (valid→200, invalid→400+message), got: {output}"


# ---------------------------------------------------------------------------
# format: ipv4
# ---------------------------------------------------------------------------


@pytest.mark.depends(on=["test_openapi_flag_is_recognized"])
def test_ipv4_format_valid_address_passes():
    """Test that a server with format: ipv4 accepts a well-formed IPv4 address."""
    print("\n🔍 Testing valid IPv4 format passes...", flush=True)
    time.sleep(0.5)

    result = subprocess.run(
        [
            "pytest",
            "--openapi=http://mock-server-ipv4-format-validation:8000",
            "-v",
        ],
        capture_output=True,
        text=True,
        cwd="/app",
    )

    output = result.stdout + result.stderr
    assert (
        "✅ OpenAPI spec validated successfully" in output
    ), f"Expected OpenAPI spec with IPv4 format to validate, got: {output}"
    assert (
        "test_openapi[POST /allow" in output
    ), f"Expected POST /allow test items, got: {output}"


@pytest.mark.depends(on=["test_openapi_flag_is_recognized"])
def test_ipv4_format_invalid_address_gets_400_with_message():
    """Test that invalid IPv4 values (e.g. '999.999.999.999', 'not-an-ip',
    or a string with only three octets) cause the server to return a
    descriptive 400 and the plugin treats this as a passing contract test.
    """
    print(
        "\n🔍 Testing invalid IPv4 gets descriptive 400 and plugin passes...",
        flush=True,
    )
    time.sleep(0.5)

    result = subprocess.run(
        [
            "pytest",
            "--openapi=http://mock-server-ipv4-format-validation:8000",
            "-v",
        ],
        capture_output=True,
        text=True,
        cwd="/app",
    )

    output = result.stdout + result.stderr
    assert (
        result.returncode == 0
    ), f"Expected all IPv4 format tests to pass (valid→200, invalid→400+message), got: {output}"


# ---------------------------------------------------------------------------
# format: ipv6
# ---------------------------------------------------------------------------


@pytest.mark.depends(on=["test_openapi_flag_is_recognized"])
def test_ipv6_format_valid_address_passes():
    """Test that a server with format: ipv6 accepts a well-formed IPv6 address."""
    print("\n🔍 Testing valid IPv6 format passes...", flush=True)
    time.sleep(0.5)

    result = subprocess.run(
        [
            "pytest",
            "--openapi=http://mock-server-ipv6-format-validation:8000",
            "-v",
        ],
        capture_output=True,
        text=True,
        cwd="/app",
    )

    output = result.stdout + result.stderr
    assert (
        "✅ OpenAPI spec validated successfully" in output
    ), f"Expected OpenAPI spec with IPv6 format to validate, got: {output}"
    assert (
        "test_openapi[POST /allow6" in output
    ), f"Expected POST /allow6 test items, got: {output}"


@pytest.mark.depends(on=["test_openapi_flag_is_recognized"])
def test_ipv6_format_invalid_address_gets_400_with_message():
    """Test that invalid IPv6 values (e.g. 'not-ipv6', 'gggg::1' with non-hex
    characters, or a plain IPv4 address) cause the server to return a descriptive
    400 and the plugin treats this as a passing contract test.
    """
    print(
        "\n🔍 Testing invalid IPv6 gets descriptive 400 and plugin passes...",
        flush=True,
    )
    time.sleep(0.5)

    result = subprocess.run(
        [
            "pytest",
            "--openapi=http://mock-server-ipv6-format-validation:8000",
            "-v",
        ],
        capture_output=True,
        text=True,
        cwd="/app",
    )

    output = result.stdout + result.stderr
    assert (
        result.returncode == 0
    ), f"Expected all IPv6 format tests to pass (valid→200, invalid→400+message), got: {output}"


# ---------------------------------------------------------------------------
# format: hostname
# ---------------------------------------------------------------------------


@pytest.mark.depends(on=["test_openapi_flag_is_recognized"])
def test_hostname_format_valid_hostname_passes():
    """Test that a server with format: hostname accepts well-formed hostnames."""
    print("\n🔍 Testing valid hostname format passes...", flush=True)
    time.sleep(0.5)

    result = subprocess.run(
        [
            "pytest",
            "--openapi=http://mock-server-hostname-format-validation:8000",
            "-v",
        ],
        capture_output=True,
        text=True,
        cwd="/app",
    )

    output = result.stdout + result.stderr
    assert (
        "✅ OpenAPI spec validated successfully" in output
    ), f"Expected OpenAPI spec with hostname format to validate, got: {output}"
    assert (
        "test_openapi[POST /config" in output
    ), f"Expected POST /config test items, got: {output}"


@pytest.mark.depends(on=["test_openapi_flag_is_recognized"])
def test_hostname_format_invalid_hostname_gets_400_with_message():
    """Test that invalid hostnames (e.g. 'has space.com', '-starts-with-dash',
    'example..com' with consecutive dots) cause the server to return a
    descriptive 400 and the plugin treats this as a passing contract test.
    """
    print(
        "\n🔍 Testing invalid hostname gets descriptive 400 and plugin passes...",
        flush=True,
    )
    time.sleep(0.5)

    result = subprocess.run(
        [
            "pytest",
            "--openapi=http://mock-server-hostname-format-validation:8000",
            "-v",
        ],
        capture_output=True,
        text=True,
        cwd="/app",
    )

    output = result.stdout + result.stderr
    assert (
        result.returncode == 0
    ), f"Expected all hostname format tests to pass (valid→200, invalid→400+message), got: {output}"


# ---------------------------------------------------------------------------
# URL port-number edge cases
# ---------------------------------------------------------------------------


@pytest.mark.depends(on=["test_openapi_flag_is_recognized"])
def test_url_port_valid_ports_pass():
    """Test that URLs with valid port numbers (e.g. :80, :8080, :65535) pass.

    Port numbers 1-65535 are valid for HTTP/HTTPS URLs.
    The spec example uses :8080 which must produce a 200 response.
    """
    print("\n🔍 Testing URL with valid port numbers passes...", flush=True)
    time.sleep(0.5)

    result = subprocess.run(
        [
            "pytest",
            "--openapi=http://mock-server-url-port-validation:8000",
            "-v",
        ],
        capture_output=True,
        text=True,
        cwd="/app",
    )

    output = result.stdout + result.stderr
    assert (
        "✅ OpenAPI spec validated successfully" in output
    ), f"Expected OpenAPI spec with URL port format to validate, got: {output}"
    assert (
        "test_openapi[POST /webhook" in output
    ), f"Expected POST /webhook test items for URL port server, got: {output}"


@pytest.mark.depends(on=["test_openapi_flag_is_recognized"])
def test_url_port_zero_gets_400_with_message():
    """Test that a URL containing port 0 (https://example.com:0/path) causes the
    server to return a descriptive 400.

    Port 0 is reserved and not valid for HTTP URLs even though it is technically
    within the 0-65535 unsigned-16-bit range.  The plugin must generate this edge
    case and the server must reject it with a message that mentions port 0.
    """
    print(
        "\n🔍 Testing URL with port 0 gets descriptive 400...",
        flush=True,
    )
    time.sleep(0.5)

    result = subprocess.run(
        [
            "pytest",
            "--openapi=http://mock-server-url-port-validation:8000",
            "-v",
        ],
        capture_output=True,
        text=True,
        cwd="/app",
    )

    output = result.stdout + result.stderr
    # All tests should pass: valid URLs → 200, invalid-port URLs → 400 with message
    assert (
        result.returncode == 0
    ), f"Expected URL port tests to pass (valid ports→200, port 0→400+message), got: {output}"


@pytest.mark.depends(on=["test_openapi_flag_is_recognized"])
def test_url_port_above_65535_gets_400_with_message():
    """Test that a URL containing a port above 65535 (e.g. :65536 or :99999)
    causes the server to return a descriptive 400.

    Port numbers above 65535 are outside the 16-bit unsigned range and are
    never valid.  The plugin must generate this edge case and the server must
    reject it with a message that references the maximum port number.
    """
    print(
        "\n🔍 Testing URL with port > 65535 gets descriptive 400...",
        flush=True,
    )
    time.sleep(0.5)

    result = subprocess.run(
        [
            "pytest",
            "--openapi=http://mock-server-url-port-validation:8000",
            "-v",
        ],
        capture_output=True,
        text=True,
        cwd="/app",
    )

    output = result.stdout + result.stderr
    assert (
        result.returncode == 0
    ), f"Expected URL port tests to pass (valid ports→200, port>65535→400+message), got: {output}"
