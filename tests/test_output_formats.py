"""Integration tests for pytest-openapi output format options."""

import subprocess
import time
import pytest
import os
import tempfile


@pytest.mark.depends(on=["test_integration.py::test_openapi_flag_is_recognized"])
def test_markdown_output_to_file():
    """Test that --openapi-markdown-output writes Markdown to a file."""
    print("\n🔍 Testing Markdown output to file...", flush=True)
    time.sleep(0.5)

    with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as tmp:
        tmp_path = tmp.name

    try:
        result = subprocess.run(
            [
                "pytest",
                "--openapi=http://mock-server-valid-api:8000",
                f"--openapi-markdown-output={tmp_path}",
                "-v",
            ],
            capture_output=True,
            text=True,
            cwd="/app",
        )

        # Check that the file was created
        assert os.path.exists(tmp_path), f"Expected markdown file to be created at {tmp_path}"

        # Read the file content
        with open(tmp_path, 'r') as f:
            file_content = f.read()

        # Check for Markdown formatting elements in the file
        assert (
            "# OpenAPI Contract Test Report" in file_content
        ), f"Expected Markdown header in file, got: {file_content}"

        assert (
            "## Summary" in file_content
        ), f"Expected Markdown summary section in file, got: {file_content}"

        assert (
            "**Total Tests:**" in file_content
        ), f"Expected Markdown formatted test count in file, got: {file_content}"

        assert (
            "```json" in file_content
        ), f"Expected Markdown JSON code blocks in file, got: {file_content}"

        # Stdout should still show the normal report
        output = result.stdout + result.stderr
        assert (
            "OpenAPI Contract Test Report" in output
        ), f"Expected normal report in stdout, got: {output}"

        # Should show confirmation message
        assert (
            f"📝 Markdown report written to: {tmp_path}" in output
        ), f"Expected confirmation message in output, got: {output}"

        # Should still pass all tests
        assert (
            result.returncode == 0
        ), f"Expected tests to pass with markdown output, got: {output}"
    finally:
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)


@pytest.mark.depends(on=["test_integration.py::test_openapi_flag_is_recognized"])
def test_markdown_output_with_failures():
    """Test that --openapi-markdown-output properly formats test failures in file."""
    print("\n🔍 Testing Markdown output format with failures...", flush=True)
    time.sleep(0.5)

    with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as tmp:
        tmp_path = tmp.name

    try:
        result = subprocess.run(
            [
                "pytest",
                "--openapi=http://mock-server-get-missing-key:8000",
                f"--openapi-markdown-output={tmp_path}",
                "-v",
            ],
            capture_output=True,
            text=True,
            cwd="/app",
        )

        # Check that the file was created
        assert os.path.exists(tmp_path), f"Expected markdown file to be created at {tmp_path}"

        # Read the file content
        with open(tmp_path, 'r') as f:
            file_content = f.read()

        # Check for Markdown formatting with failures in file
        assert (
            "# OpenAPI Contract Test Report" in file_content
        ), f"Expected Markdown header in file, got: {file_content}"

        assert (
            "❌" in file_content
        ), f"Expected failure symbol in Markdown file, got: {file_content}"

        assert (
            "### ❌ Error" in file_content
        ), f"Expected Markdown error section in file, got: {file_content}"

        # Should fail as expected
        assert (
            result.returncode != 0
        ), f"Expected tests to fail for missing key test"
    finally:
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)


@pytest.mark.depends(on=["test_integration.py::test_openapi_flag_is_recognized"])
def test_no_stdout():
    """Test that --openapi-no-stdout suppresses all stdout."""
    print("\n🔍 Testing stdout suppression...", flush=True)
    time.sleep(0.5)

    result = subprocess.run(
        [
            "pytest",
            "--openapi=http://mock-server-valid-api:8000",
            "--openapi-no-stdout",
            "-v",
        ],
        capture_output=True,
        text=True,
        cwd="/app",
    )

    output = result.stdout + result.stderr

    # The detailed report should NOT be present
    assert (
        "OpenAPI Contract Test Report" not in output
    ), f"Expected detailed report to be suppressed, but found it in output: {output}"

    # The success message should also be suppressed
    assert (
        "✅ All contract tests passed!" not in output
    ), f"Expected success message to be suppressed, got: {output}"

    # Should still pass
    assert (
        result.returncode == 0
    ), f"Expected tests to pass with no-stdout, got: {output}"


@pytest.mark.depends(on=["test_integration.py::test_openapi_flag_is_recognized"])
def test_no_stdout_with_failures():
    """Test that --openapi-no-stdout suppresses all stdout even with failures."""
    print("\n🔍 Testing stdout suppression with failures...", flush=True)
    time.sleep(0.5)

    result = subprocess.run(
        [
            "pytest",
            "--openapi=http://mock-server-get-missing-key:8000",
            "--openapi-no-stdout",
            "-v",
        ],
        capture_output=True,
        text=True,
        cwd="/app",
    )

    output = result.stdout + result.stderr

    # The detailed report should NOT be present
    assert (
        "OpenAPI Contract Test Report" not in output
    ), f"Expected detailed report to be suppressed, but found it in output: {output}"

    # Error list should also be suppressed
    assert (
        "❌ Contract tests failed:" not in output
    ), f"Expected failure summary to be suppressed with no-stdout, got: {output}"

    # Should fail as expected
    assert (
        result.returncode != 0
    ), f"Expected tests to fail for missing key test"


@pytest.mark.depends(on=["test_integration.py::test_openapi_flag_is_recognized"])
def test_markdown_and_no_stdout_combined():
    """Test that --openapi-markdown-output with --openapi-no-stdout writes file without stdout."""
    print("\n🔍 Testing combined Markdown file and no stdout...", flush=True)
    time.sleep(0.5)

    with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as tmp:
        tmp_path = tmp.name

    try:
        result = subprocess.run(
            [
                "pytest",
                "--openapi=http://mock-server-valid-api:8000",
                f"--openapi-markdown-output={tmp_path}",
                "--openapi-no-stdout",
                "-v",
            ],
            capture_output=True,
            text=True,
            cwd="/app",
        )

        output = result.stdout + result.stderr

        # Stdout should be completely suppressed
        assert (
            "OpenAPI Contract Test Report" not in output
        ), f"Expected no report in stdout, got: {output}"

        assert (
            "# OpenAPI Contract Test Report" not in output
        ), f"Expected no Markdown in stdout, got: {output}"

        assert (
            "✅ All contract tests passed!" not in output
        ), f"Expected no success message in stdout, got: {output}"

        # Should not show confirmation message either
        assert (
            "📝 Markdown report written to:" not in output
        ), f"Expected no confirmation message with no-stdout, got: {output}"

        # But the file should still be created
        assert os.path.exists(tmp_path), f"Expected markdown file to be created at {tmp_path}"

        # And contain the report
        with open(tmp_path, 'r') as f:
            file_content = f.read()

        assert (
            "# OpenAPI Contract Test Report" in file_content
        ), f"Expected Markdown header in file, got: {file_content}"

        # Should pass
        assert (
            result.returncode == 0
        ), f"Expected tests to pass"
    finally:
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)


@pytest.mark.depends(on=["test_integration.py::test_openapi_flag_is_recognized"])
def test_default_output_unchanged():
    """Test that default output (without flags) remains unchanged."""
    print("\n🔍 Testing default output format...", flush=True)
    time.sleep(0.5)

    result = subprocess.run(
        [
            "pytest",
            "--openapi=http://mock-server-valid-api:8000",
            "-v",
        ],
        capture_output=True,
        text=True,
        cwd="/app",
    )

    output = result.stdout + result.stderr

    # Should have the standard report format (not Markdown)
    assert (
        "=" * 80 in output or "OpenAPI Contract Test Report" in output
    ), f"Expected standard report format in output, got: {output}"

    # Should not have Markdown headers
    assert (
        "# OpenAPI Contract Test Report" not in output
    ), f"Expected no Markdown formatting in default output, got: {output}"

    # Should show success message
    assert (
        "✅ All contract tests passed!" in output
        or "✅ OpenAPI spec validated successfully" in output
    ), f"Expected success message in default output, got: {output}"

    # Should pass
    assert (
        result.returncode == 0
    ), f"Expected tests to pass with default output, got: {output}"


@pytest.mark.depends(on=["test_integration.py::test_openapi_flag_is_recognized"])
def test_pytest_depends_compatibility():
    """Test that pytest-openapi works with pytest-depends without IndexError."""
    print("\n🔍 Testing pytest-depends compatibility...", flush=True)
    time.sleep(0.5)

    # This test itself uses pytest-depends, so if we get here without
    # IndexError in pytest_unconfigure, the fix is working
    result = subprocess.run(
        [
            "pytest",
            "--openapi=http://mock-server-valid-api:8000",
            "-v",
        ],
        capture_output=True,
        text=True,
        cwd="/app",
    )

    output = result.stdout + result.stderr

    # Should not have IndexError
    assert (
        "IndexError: pop from empty list" not in output
    ), f"Expected no IndexError from pytest-depends, got: {output}"

    # Should not have pytest_unconfigure error
    assert (
        "pytest_unconfigure" not in output or result.returncode == 0
    ), f"Expected no pytest_unconfigure errors, got: {output}"

