import os
import json
import time

import pytest


def test_unit():
    assert True


def test_schema_based_test_case_generation():
    """Test that test case generation from schemas works correctly."""
    from pytest_openapi.case_generator import generate_test_cases_for_schema

    # Test string with format
    schema = {"type": "string", "format": "email"}
    test_cases, warnings = generate_test_cases_for_schema(schema)
    assert len(test_cases) > 0
    assert "@" in test_cases[0]  # Should be an email

    # Test integer with constraints
    schema = {"type": "integer", "minimum": 5, "maximum": 10}
    test_cases, warnings = generate_test_cases_for_schema(schema)
    assert len(test_cases) >= 3  # boundary + middle
    assert all(5 <= x <= 10 for x in test_cases)

    # Test number with constraints
    schema = {"type": "number", "minimum": 0.0, "maximum": 1.0}
    test_cases, warnings = generate_test_cases_for_schema(schema)
    assert len(test_cases) > 0
    assert all(0.0 <= x <= 1.0 for x in test_cases)

    # Test boolean
    schema = {"type": "boolean"}
    test_cases, warnings = generate_test_cases_for_schema(schema)
    assert len(test_cases) == 2
    assert True in test_cases
    assert False in test_cases

    # Test object with properties
    schema = {
        "type": "object",
        "properties": {
            "name": {"type": "string"},
            "age": {"type": "integer", "minimum": 0, "maximum": 120},
        },
    }
    test_cases, warnings = generate_test_cases_for_schema(schema)
    assert len(test_cases) > 0
    assert "name" in test_cases[0]
    assert "age" in test_cases[0]
    assert isinstance(test_cases[0]["name"], str)
    assert isinstance(test_cases[0]["age"], int)
    assert 0 <= test_cases[0]["age"] <= 120

    # Test array
    schema = {
        "type": "array",
        "items": {"type": "string"},
        "minItems": 1,
        "maxItems": 3,
    }
    test_cases, warnings = generate_test_cases_for_schema(schema)
    assert len(test_cases) > 0
    assert isinstance(test_cases[0], list)
    assert 1 <= len(test_cases[0]) <= 3

    # Test enum
    schema = {"type": "string", "enum": ["red", "green", "blue"]}
    test_cases, warnings = generate_test_cases_for_schema(schema)
    assert len(test_cases) == 3
    assert set(test_cases) == {"red", "green", "blue"}


def test_string_edge_cases():
    """Test that string generation includes edge cases."""
    from pytest_openapi.case_generator import generate_string_test_cases

    schema = {"type": "string"}
    test_cases = generate_string_test_cases(schema)

    # Should have several test cases
    assert len(test_cases) >= 5

    # Check for edge cases (at least some should be present)
    test_cases_str = " ".join(str(e) for e in test_cases)
    # We expect variety: quotes, special chars, etc.
    assert any(
        '"' in str(e) or "'" in str(e) or ":" in str(e) for e in test_cases
    )


def test_integer_boundary_testing():
    """Test that integer generation respects boundaries."""
    from pytest_openapi.case_generator import generate_integer_test_cases

    # Test with minimum and maximum
    schema = {"type": "integer", "minimum": 10, "maximum": 20}
    test_cases, warnings = generate_integer_test_cases(schema)
    assert 10 in test_cases  # Lower boundary
    assert 20 in test_cases  # Upper boundary
    assert any(10 < x < 20 for x in test_cases)  # Middle value

    # Test with exclusiveMinimum and exclusiveMaximum
    schema = {"type": "integer", "exclusiveMinimum": 10, "exclusiveMaximum": 20}
    test_cases, warnings = generate_integer_test_cases(schema)
    assert 10 not in test_cases
    assert 20 not in test_cases
    assert all(10 < x < 20 for x in test_cases)

    # Test multipleOf
    schema = {"type": "integer", "multipleOf": 5, "minimum": 0, "maximum": 50}
    test_cases, warnings = generate_integer_test_cases(schema)
    assert all(x % 5 == 0 for x in test_cases)
