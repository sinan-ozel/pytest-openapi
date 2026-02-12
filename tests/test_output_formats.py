"""Integration tests for pytest-openapi output format options."""

import subprocess
import time
import pytest
import os
import tempfile


@pytest.mark.depends(
    on=["test_integration.py::test_openapi_flag_is_recognized"]
)
def test_markdown_output_to_file():
    """Test that --openapi-markdown-output writes Markdown to a file."""
    print("\n🔍 Testing Markdown output to file...", flush=True)
    time.sleep(0.5)

    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".md", delete=False
    ) as tmp:
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
        assert os.path.exists(
            tmp_path
        ), f"Expected markdown file to be created at {tmp_path}"

        # Read the file content
        with open(tmp_path, "r") as f:
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

        # Stdout should show individual pytest test items
        output = result.stdout + result.stderr
        assert (
            "test_openapi[" in output
        ), f"Expected individual test items in stdout, got: {output}"

        # Should show confirmation message about markdown file
        assert (
            f"📝 Full test report saved to: {tmp_path}" in output
        ), f"Expected confirmation message in output, got: {output}"

        # Should still pass all tests
        assert (
            result.returncode == 0
        ), f"Expected tests to pass with markdown output, got: {output}"
    finally:
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)


@pytest.mark.depends(
    on=["test_integration.py::test_openapi_flag_is_recognized"]
)
def test_markdown_output_with_failures():
    """Test that --openapi-markdown-output properly formats test failures in file."""
    print("\n🔍 Testing Markdown output format with failures...", flush=True)
    time.sleep(0.5)

    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".md", delete=False
    ) as tmp:
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
        assert os.path.exists(
            tmp_path
        ), f"Expected markdown file to be created at {tmp_path}"

        # Read the file content
        with open(tmp_path, "r") as f:
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


@pytest.mark.depends(
    on=["test_integration.py::test_openapi_flag_is_recognized"]
)
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

    # The plugin-specific messages should be suppressed with --openapi-no-stdout
    assert (
        "📝 Full test report saved to:" not in output
    ), f"Expected report message to be suppressed, but found it in output: {output}"

    # But pytest output should still be present showing test results
    assert (
        "test_openapi[" in output or "passed" in output.lower()
    ), f"Expected pytest test output to be present, got: {output}"

    # Should still pass
    assert (
        result.returncode == 0
    ), f"Expected tests to pass with no-stdout, got: {output}"


@pytest.mark.depends(
    on=["test_integration.py::test_openapi_flag_is_recognized"]
)
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

    # The plugin-specific messages should be suppressed
    assert (
        "📝 Full test report saved to:" not in output
    ), f"Expected report message to be suppressed, but found it in output: {output}"

    # But pytest should still show test failures
    assert (
        "FAILED" in output or "failed" in output.lower()
    ), f"Expected pytest failure output to be present, got: {output}"

    # Should fail as expected
    assert (
        result.returncode != 0
    ), f"Expected tests to fail for missing key test"


@pytest.mark.depends(
    on=["test_integration.py::test_openapi_flag_is_recognized"]
)
def test_markdown_and_no_stdout_combined():
    """Test that --openapi-markdown-output with --openapi-no-stdout writes file without stdout."""
    print("\n🔍 Testing combined Markdown file and no stdout...", flush=True)
    time.sleep(0.5)

    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".md", delete=False
    ) as tmp:
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

        # Plugin messages should be suppressed with --openapi-no-stdout
        assert (
            "📝 Full test report saved to:" not in output
        ), f"Expected no report message with no-stdout, got: {output}"

        # But pytest output should still be present
        assert (
            "test session starts" in output or "passed" in output.lower()
        ), f"Expected pytest output to be present, got: {output}"

        # But the file should still be created
        assert os.path.exists(
            tmp_path
        ), f"Expected markdown file to be created at {tmp_path}"

        # And contain the report
        with open(tmp_path, "r") as f:
            file_content = f.read()

        assert (
            "# OpenAPI Contract Test Report" in file_content
        ), f"Expected Markdown header in file, got: {file_content}"

        # Should pass
        assert result.returncode == 0, f"Expected tests to pass"
    finally:
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)


@pytest.mark.depends(
    on=["test_integration.py::test_openapi_flag_is_recognized"]
)
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

    # Should have pytest's standard output showing individual test items
    assert (
        "test session starts" in output
    ), f"Expected pytest session output, got: {output}"

    # Should show individual test items
    assert (
        "test_openapi[" in output
    ), f"Expected individual test items in output, got: {output}"

    # Should show validation success
    assert (
        "✅ OpenAPI spec validated successfully" in output
    ), f"Expected validation message in default output, got: {output}"

    # Should pass
    assert (
        result.returncode == 0
    ), f"Expected tests to pass with default output, got: {output}"


@pytest.mark.depends(
    on=["test_integration.py::test_openapi_flag_is_recognized"]
)
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


@pytest.mark.depends(
    on=["test_integration.py::test_openapi_flag_is_recognized"]
)
def test_markdown_file_created_with_correct_name():
    """Test that markdown file is created with the exact filename specified."""
    print(
        "\n🔍 Testing markdown file creation with correct name...", flush=True
    )
    time.sleep(0.5)

    custom_filename = "my_custom_report.md"
    tmp_dir = tempfile.mkdtemp()
    tmp_path = os.path.join(tmp_dir, custom_filename)

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

        # Check that the file was created with exact name
        assert os.path.exists(
            tmp_path
        ), f"Expected markdown file to be created at {tmp_path}"

        # Check that the filename is correct
        assert os.path.basename(tmp_path) == custom_filename, (
            f"Expected filename to be {custom_filename}, "
            f"got {os.path.basename(tmp_path)}"
        )

        # Verify the path in the output message
        output = result.stdout + result.stderr
        assert (
            tmp_path in output
        ), f"Expected exact path {tmp_path} in output, got: {output}"

    finally:
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)
        if os.path.exists(tmp_dir):
            os.rmdir(tmp_dir)


@pytest.mark.depends(
    on=["test_integration.py::test_openapi_flag_is_recognized"]
)
def test_markdown_counts_match_actual_tests():
    """Test that markdown summary counts match the actual test execution counts."""
    print("\n🔍 Testing markdown counts match actual tests...", flush=True)
    time.sleep(0.5)

    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".md", delete=False
    ) as tmp:
        tmp_path = tmp.name

    try:
        result = subprocess.run(
            [
                "pytest",
                "--openapi=http://mock-server-valid-api:8000",
                f"--openapi-markdown-output={tmp_path}",
                "--ignore=/app/test_samples",  # Only run OpenAPI tests
                "-v",
            ],
            capture_output=True,
            text=True,
            cwd="/app",
        )

        output = result.stdout + result.stderr

        # Read the markdown file
        with open(tmp_path, "r") as f:
            file_content = f.read()

        # Extract counts from pytest output
        # Look for pattern like "24 passed in X.XXs"
        import re

        pytest_match = re.search(r"(\d+) passed", output)
        assert pytest_match, f"Could not find passed count in output: {output}"
        pytest_passed = int(pytest_match.group(1))

        # Extract counts from markdown summary
        # Look for "- **Passed:** ✅ 24"
        md_passed_match = re.search(r"\*\*Passed:\*\* ✅ (\d+)", file_content)
        assert (
            md_passed_match
        ), f"Could not find passed count in markdown: {file_content}"
        md_passed = int(md_passed_match.group(1))

        # Extract total from markdown
        md_total_match = re.search(r"\*\*Total Tests:\*\* (\d+)", file_content)
        assert (
            md_total_match
        ), f"Could not find total count in markdown: {file_content}"
        md_total = int(md_total_match.group(1))

        # Verify counts match
        assert pytest_passed == md_passed, (
            f"Passed count mismatch: pytest shows {pytest_passed}, "
            f"markdown shows {md_passed}"
        )

        # Verify total equals passed (since all should pass)
        assert md_total == md_passed, (
            f"Total {md_total} should equal passed {md_passed} "
            f"when all tests pass"
        )

        # Verify failed count is 0
        md_failed_match = re.search(r"\*\*Failed:\*\* ❌ (\d+)", file_content)
        assert (
            md_failed_match
        ), f"Could not find failed count in markdown: {file_content}"
        md_failed = int(md_failed_match.group(1))
        assert md_failed == 0, f"Expected 0 failed tests, got {md_failed}"

    finally:
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)


@pytest.mark.depends(
    on=["test_integration.py::test_openapi_flag_is_recognized"]
)
def test_markdown_counts_with_failures():
    """Test that markdown summary correctly counts passed and failed tests."""
    print("\n🔍 Testing markdown counts with failures...", flush=True)
    time.sleep(0.5)

    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".md", delete=False
    ) as tmp:
        tmp_path = tmp.name

    try:
        result = subprocess.run(
            [
                "pytest",
                "--openapi=http://mock-server-get-missing-key:8000",
                f"--openapi-markdown-output={tmp_path}",
                "--ignore=/app/test_samples",  # Only run OpenAPI tests
                "-v",
            ],
            capture_output=True,
            text=True,
            cwd="/app",
        )

        output = result.stdout + result.stderr

        # Read the markdown file
        with open(tmp_path, "r") as f:
            file_content = f.read()

        # Extract counts from pytest output
        import re

        pytest_passed_match = re.search(r"(\d+) passed", output)
        pytest_failed_match = re.search(r"(\d+) failed", output)

        assert (
            pytest_passed_match or pytest_failed_match
        ), f"Could not find test counts in output: {output}"

        pytest_passed = (
            int(pytest_passed_match.group(1)) if pytest_passed_match else 0
        )
        pytest_failed = (
            int(pytest_failed_match.group(1)) if pytest_failed_match else 0
        )
        pytest_total = pytest_passed + pytest_failed

        # Extract counts from markdown
        md_total_match = re.search(r"\*\*Total Tests:\*\* (\d+)", file_content)
        md_passed_match = re.search(r"\*\*Passed:\*\* ✅ (\d+)", file_content)
        md_failed_match = re.search(r"\*\*Failed:\*\* ❌ (\d+)", file_content)

        assert (
            md_total_match
        ), f"Could not find total in markdown: {file_content}"
        assert (
            md_passed_match
        ), f"Could not find passed in markdown: {file_content}"
        assert (
            md_failed_match
        ), f"Could not find failed in markdown: {file_content}"

        md_total = int(md_total_match.group(1))
        md_passed = int(md_passed_match.group(1))
        md_failed = int(md_failed_match.group(1))

        # Verify counts match
        assert pytest_total == md_total, (
            f"Total count mismatch: pytest shows {pytest_total}, "
            f"markdown shows {md_total}"
        )
        assert pytest_passed == md_passed, (
            f"Passed count mismatch: pytest shows {pytest_passed}, "
            f"markdown shows {md_passed}"
        )
        assert pytest_failed == md_failed, (
            f"Failed count mismatch: pytest shows {pytest_failed}, "
            f"markdown shows {md_failed}"
        )

        # Verify total = passed + failed
        assert md_total == md_passed + md_failed, (
            f"Total {md_total} should equal passed {md_passed} + "
            f"failed {md_failed} = {md_passed + md_failed}"
        )

    finally:
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)
