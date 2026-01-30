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

    # Test enum - should include valid values + one invalid
    schema = {"type": "string", "enum": ["red", "green", "blue"]}
    test_cases, warnings = generate_test_cases_for_schema(schema)
    assert len(test_cases) == 4  # 3 valid + 1 invalid
    # Check that all valid values are present
    assert "red" in test_cases
    assert "green" in test_cases
    assert "blue" in test_cases
    # Check that there's one invalid value (not in the original enum)
    invalid_values = [
        v for v in test_cases if v not in ["red", "green", "blue"]
    ]
    assert len(invalid_values) == 1


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


def test_validate_nullable_fields():
    """Test that nullable fields are properly validated for both OpenAPI 3.0 and 3.1."""
    from pytest_openapi.contract import validate_against_schema

    # OpenAPI 3.0 style: nullable: true
    schema_3_0 = {"type": "string", "nullable": True}
    valid, error = validate_against_schema(schema_3_0, None)
    assert valid, f"Should accept null for nullable field (3.0): {error}"

    valid, error = validate_against_schema(schema_3_0, "test_string")
    assert (
        valid
    ), f"Should accept string for nullable string field (3.0): {error}"

    # OpenAPI 3.1 style: type: ["string", "null"]
    schema_3_1 = {"type": ["string", "null"]}
    valid, error = validate_against_schema(schema_3_1, None)
    assert valid, f"Should accept null for nullable field (3.1): {error}"

    valid, error = validate_against_schema(schema_3_1, "test_string")
    assert (
        valid
    ), f"Should accept string for nullable string field (3.1): {error}"

    # Test with integer nullable
    schema_3_0_int = {"type": "integer", "nullable": True}
    valid, error = validate_against_schema(schema_3_0_int, None)
    assert (
        valid
    ), f"Should accept null for nullable integer field (3.0): {error}"

    valid, error = validate_against_schema(schema_3_0_int, 42)
    assert (
        valid
    ), f"Should accept integer for nullable integer field (3.0): {error}"

    schema_3_1_int = {"type": ["integer", "null"]}
    valid, error = validate_against_schema(schema_3_1_int, None)
    assert (
        valid
    ), f"Should accept null for nullable integer field (3.1): {error}"

    valid, error = validate_against_schema(schema_3_1_int, 42)
    assert (
        valid
    ), f"Should accept integer for nullable integer field (3.1): {error}"

    # Test that non-nullable fields still reject null
    schema_not_nullable = {"type": "string"}
    valid, error = validate_against_schema(schema_not_nullable, None)
    assert not valid, "Should reject null for non-nullable field"
    assert "Expected string, got NoneType" in error

    # Test in object context (like the user's example)
    schema_object = {
        "type": "object",
        "properties": {
            "available": {"type": "array", "items": {"type": "string"}},
            "default": {"type": "string", "nullable": True},
            "total": {"type": "integer"},
            "status": {"type": "string"},
        },
        "required": ["available", "total", "status"],
    }

    response_with_null = {
        "available": [],
        "default": None,
        "total": 12,
        "status": "no_providers_available",
    }

    valid, error = validate_against_schema(schema_object, response_with_null)
    assert valid, f"Should accept response with null nullable field: {error}"

    # Same test with OpenAPI 3.1 syntax
    schema_object_3_1 = {
        "type": "object",
        "properties": {
            "available": {"type": "array", "items": {"type": "string"}},
            "default": {"type": ["string", "null"]},
            "total": {"type": "integer"},
            "status": {"type": "string"},
        },
        "required": ["available", "total", "status"],
    }

    valid, error = validate_against_schema(
        schema_object_3_1, response_with_null
    )
    assert (
        valid
    ), f"Should accept response with null nullable field (3.1): {error}"


def test_validate_enum_fields():
    """Test that enum fields are properly validated."""
    from pytest_openapi.contract import validate_against_schema

    # Test string enum
    schema_string_enum = {
        "type": "string",
        "enum": ["option1", "option2", "option3"],
    }

    # Valid enum value
    valid, error = validate_against_schema(schema_string_enum, "option1")
    assert valid, f"Should accept valid enum value: {error}"

    valid, error = validate_against_schema(schema_string_enum, "option2")
    assert valid, f"Should accept valid enum value: {error}"

    # Invalid enum value
    valid, error = validate_against_schema(schema_string_enum, "invalid_option")
    assert not valid, "Should reject invalid enum value"
    assert "not one of the allowed enum values" in error
    assert "['option1', 'option2', 'option3']" in error

    # Test integer enum
    schema_integer_enum = {"type": "integer", "enum": [1, 2, 3, 5, 8]}

    valid, error = validate_against_schema(schema_integer_enum, 5)
    assert valid, f"Should accept valid integer enum value: {error}"

    valid, error = validate_against_schema(schema_integer_enum, 4)
    assert not valid, "Should reject invalid integer enum value"
    assert "not one of the allowed enum values" in error

    # Test enum in object property
    schema_object_with_enum = {
        "type": "object",
        "properties": {
            "name": {"type": "string"},
            "status": {
                "type": "string",
                "enum": ["active", "inactive", "pending"],
            },
            "priority": {"type": "integer", "enum": [1, 2, 3]},
        },
        "required": ["name", "status"],
    }

    # Valid object with enum values
    valid_response = {"name": "Test Item", "status": "active", "priority": 2}
    valid, error = validate_against_schema(
        schema_object_with_enum, valid_response
    )
    assert valid, f"Should accept object with valid enum values: {error}"

    # Invalid object with bad status enum
    invalid_status_response = {
        "name": "Test Item",
        "status": "deleted",
        "priority": 2,
    }
    valid, error = validate_against_schema(
        schema_object_with_enum, invalid_status_response
    )
    assert not valid, "Should reject object with invalid enum value"
    assert "status" in error
    assert "not one of the allowed enum values" in error

    # Invalid object with bad priority enum
    invalid_priority_response = {
        "name": "Test Item",
        "status": "active",
        "priority": 5,
    }
    valid, error = validate_against_schema(
        schema_object_with_enum, invalid_priority_response
    )
    assert not valid, "Should reject object with invalid enum value"
    assert "priority" in error
    assert "not one of the allowed enum values" in error

    # Test enum in array items
    schema_array_with_enum = {
        "type": "array",
        "items": {"type": "string", "enum": ["red", "green", "blue"]},
    }

    valid, error = validate_against_schema(
        schema_array_with_enum, ["red", "blue", "green"]
    )
    assert valid, f"Should accept array with valid enum values: {error}"

    valid, error = validate_against_schema(
        schema_array_with_enum, ["red", "yellow", "blue"]
    )
    assert not valid, "Should reject array with invalid enum value"
    assert "not one of the allowed enum values" in error


def test_negative_enum_test_cases_generated():
    """Test that invalid enum values are generated as negative test cases."""
    from pytest_openapi.case_generator import generate_test_cases_for_schema

    # Test string enum
    schema = {"type": "string", "enum": ["option1", "option2", "option3"]}
    test_cases, _ = generate_test_cases_for_schema(schema)

    # Should have 3 valid + 1 invalid = 4 total
    assert len(test_cases) == 4
    assert "option1" in test_cases
    assert "option2" in test_cases
    assert "option3" in test_cases

    # Find the invalid one
    invalid_cases = [
        tc for tc in test_cases if tc not in ["option1", "option2", "option3"]
    ]
    assert len(invalid_cases) == 1
    print(f"Generated invalid enum value: {invalid_cases[0]}")

    # Test integer enum
    schema_int = {"type": "integer", "enum": [1, 2, 3]}
    test_cases_int, _ = generate_test_cases_for_schema(schema_int)

    # Should have 3 valid + 1 invalid = 4 total
    assert len(test_cases_int) == 4
    assert 1 in test_cases_int
    assert 2 in test_cases_int
    assert 3 in test_cases_int

    # Find the invalid one
    invalid_int = [tc for tc in test_cases_int if tc not in [1, 2, 3]]
    assert len(invalid_int) == 1
    print(f"Generated invalid integer enum value: {invalid_int[0]}")


def test_contains_invalid_enum_value():
    """Test the helper function that detects invalid enum values in request data."""
    from pytest_openapi.contract import contains_invalid_enum_value

    # Simple enum field
    schema = {"type": "string", "enum": ["active", "inactive"]}
    assert not contains_invalid_enum_value(schema, "active")
    assert contains_invalid_enum_value(schema, "deleted")

    # Enum in object
    schema_obj = {
        "type": "object",
        "properties": {
            "name": {"type": "string"},
            "status": {
                "type": "string",
                "enum": ["active", "inactive", "pending"],
            },
        },
    }

    valid_data = {"name": "Test", "status": "active"}
    assert not contains_invalid_enum_value(schema_obj, valid_data)

    invalid_data = {"name": "Test", "status": "deleted"}
    assert contains_invalid_enum_value(schema_obj, invalid_data)

    # Enum in array
    schema_array = {
        "type": "array",
        "items": {"type": "string", "enum": ["red", "green", "blue"]},
    }

    assert not contains_invalid_enum_value(schema_array, ["red", "blue"])
    assert contains_invalid_enum_value(schema_array, ["red", "yellow"])
