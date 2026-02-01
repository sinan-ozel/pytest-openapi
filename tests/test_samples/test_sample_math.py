"""Sample tests to verify pytest continues running regular tests after OpenAPI validation."""

import pytest


def test_sample_addition():
    """A simple test to verify pytest is running regular tests."""
    assert 1 + 1 == 2


def test_sample_multiplication():
    """Another simple test to verify pytest collects multiple tests."""
    assert 2 * 3 == 6


@pytest.mark.depends(on=["test_sample_multiplication"])
def test_sample_string_operations():
    """Test string operations."""
    assert "hello" + " " + "world" == "hello world"
    assert "pytest".upper() == "PYTEST"
