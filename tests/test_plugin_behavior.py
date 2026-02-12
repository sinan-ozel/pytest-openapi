"""Tests for pytest-openapi plugin behavior and integration with pytest."""

import subprocess
import time
import pytest


def test_openapi_plugin_runs_alongside_regular_tests():
    """Test that --openapi flag allows regular pytest tests to run alongside contract tests."""
    print(
        "\n🔍 Testing OpenAPI plugin with regular pytest tests...", flush=True
    )
    time.sleep(2)

    # This test expects that there are regular test files in /app/test_samples/
    # The plugin should:
    # 1. Run OpenAPI contract tests
    # 2. Then allow pytest to continue and run regular tests
    result = subprocess.run(
        [
            "pytest",
            "--openapi=http://mock-server-valid-api:8000",
            "/app/test_samples/",
            "-v",
        ],
        capture_output=True,
        text=True,
        cwd="/app",
    )

    output = result.stdout + result.stderr

    # Should succeed with exit code 0 (contract tests passed + regular tests passed)
    assert (
        result.returncode == 0
    ), f"Expected both OpenAPI and regular tests to pass. Expected: exit code 0, got: {result.returncode}\n\nOutput:\n{output}"

    # Check for OpenAPI validation success
    assert (
        "✅ OpenAPI spec validated successfully" in output
    ), f"Expected OpenAPI validation success, got: {output}"

    # Check that OpenAPI contract tests were collected as individual items
    assert (
        "test_openapi[GET" in output or "test_openapi[POST" in output
    ), f"Expected OpenAPI tests to appear as individual test items, got: {output}"

    # Check that regular tests were collected and ran
    assert (
        "test_samples" in output
    ), f"Expected regular test files to be collected, got: {output}"

    # Check that regular tests passed
    assert (
        "test_sample_addition" in output or "PASSED" in output
    ), f"Expected regular tests to run and pass, got: {output}"
