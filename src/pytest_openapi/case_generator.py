"""Generate test cases from OpenAPI schemas."""


def generate_string_test_cases(schema):
    """Generate string test cases from schema.

    Args:
        schema: OpenAPI schema for a string field

    Returns:
        list: List of test values
    """
    test_cases = []

    # Check for pattern (regex)
    if "pattern" in schema:
        try:
            import exrex

            # Generate a few test cases from the regex
            test_cases.extend(list(exrex.generate(schema["pattern"]))[:3])
        except ImportError:
            print(
                "⚠️  Warning: 'exrex' package not installed. Cannot generate test cases from regex patterns."
            )
            print("   Install with: pip install exrex")
            test_cases.append("test-string")
        except Exception as e:
            print(
                f"⚠️  Warning: Could not generate from pattern '{schema['pattern']}': {e}"
            )
            test_cases.append("test-string")

    # Check for enum
    elif "enum" in schema:
        test_cases.extend(schema["enum"])

    # Check for format
    elif "format" in schema:
        format_type = schema["format"]
        if format_type == "email":
            test_cases.extend(
                [
                    "test@example.com",
                    "user+tag@subdomain.example.co.uk",
                    "test.user@example.com",
                ]
            )
        elif format_type in ["ipv4", "ip"]:
            test_cases.extend(["192.168.1.1", "10.0.0.1", "127.0.0.1"])
        elif format_type == "ipv6":
            test_cases.extend(
                ["2001:0db8:85a3:0000:0000:8a2e:0370:7334", "::1", "fe80::1"]
            )
        elif format_type in ["hostname", "idn-hostname"]:
            test_cases.extend(
                ["example.com", "subdomain.example.com", "test-server.local"]
            )
        elif format_type in ["uri", "url"]:
            test_cases.extend(
                [
                    "https://example.com/path",
                    "http://localhost:8080/api/v1/resource",
                ]
            )
        elif format_type == "date":
            test_cases.extend(["2025-12-23", "2024-01-01"])
        elif format_type == "date-time":
            test_cases.extend(
                ["2025-12-23T10:30:00Z", "2024-01-01T00:00:00+00:00"]
            )
        elif format_type == "time":
            test_cases.extend(["10:30:00", "23:59:59"])
        elif format_type == "uuid":
            test_cases.extend(
                [
                    "550e8400-e29b-41d4-a716-446655440000",
                    "123e4567-e89b-12d3-a456-426614174000",
                ]
            )
        else:
            # Unknown format, use basic string
            test_cases.append(f"test-{format_type}")

    # No specific constraints, generate edge cases
    else:
        test_cases.extend(
            [
                "Lorem ipsum dolor sit amet",  # Normal text
                "Test with 'single' quotes",  # Single quotes
                'Test with "double" quotes',  # Double quotes
                "Test:with:colons",  # Colons
                "Test\\with\\backslashes",  # Backslashes
                "Test\nwith\nnewlines",  # Newlines
                "Test\r\nwith\r\nCRLF",  # Carriage returns
                "Test with UTF-8: café, naïve, 中文, 日本語",  # UTF-8
                "Test!@#$%^&*()_+-=[]{}|;:<>?,./`~",  # Special characters
                "",  # Empty string (if allowed)
            ]
        )

    # Check length constraints
    min_length = schema.get("minLength", 0)
    max_length = schema.get("maxLength")

    # Filter test cases by length
    filtered = []
    for ex in test_cases:
        if len(ex) >= min_length:
            if max_length is None or len(ex) <= max_length:
                filtered.append(ex)

    # If we have length constraints but no valid test cases, generate one
    if not filtered and (min_length > 0 or max_length is not None):
        if max_length:
            target_length = min(min_length + 5, max_length)
        else:
            target_length = min_length + 5
        filtered.append("a" * target_length)

    return filtered if filtered else ["test-string"]


def generate_integer_test_cases(schema, field_name="field"):
    """Generate integer test cases from schema.

    Args:
        schema: OpenAPI schema for an integer field
        field_name: Name of the field (for error messages)

    Returns:
        tuple: (list of test values, optional warning message)
    """
    test_cases = []
    warning = None

    # Check for enum
    if "enum" in schema:
        return schema["enum"], None

    # Get constraints
    minimum = schema.get("minimum")
    maximum = schema.get("maximum")
    exclusive_min = schema.get("exclusiveMinimum")
    exclusive_max = schema.get("exclusiveMaximum")
    multiple_of = schema.get("multipleOf", 1)
    format_type = schema.get("format")

    # Determine actual bounds
    if exclusive_min is not None:
        min_val = exclusive_min + multiple_of
    elif minimum is not None:
        min_val = minimum
    else:
        # No minimum specified
        if format_type == "int32":
            min_val = -2147483648
        elif format_type == "int64":
            min_val = -9223372036854775808
        else:
            min_val = -1000000
            warning = f"⚠️  Field '{field_name}': No minimum specified. Testing with very large negative numbers. Add 'minimum' to schema to restrict."

    if exclusive_max is not None:
        max_val = exclusive_max - multiple_of
    elif maximum is not None:
        max_val = maximum
    else:
        # No maximum specified
        if format_type == "int32":
            max_val = 2147483647
        elif format_type == "int64":
            max_val = 9223372036854775807
        else:
            max_val = 1000000
            if not warning:
                warning = f"⚠️  Field '{field_name}': No maximum specified. Testing with very large positive numbers. Add 'maximum' to schema to restrict."

    # Generate examples respecting multipleOf
    def round_to_multiple(val):
        """Round value to nearest multiple."""
        return int(round(val / multiple_of) * multiple_of)

    # Add boundary values
    test_cases.append(round_to_multiple(min_val))
    test_cases.append(round_to_multiple(max_val))

    # Add middle value
    mid_val = round_to_multiple((min_val + max_val) / 2)
    if mid_val not in test_cases:
        test_cases.append(mid_val)

    # Add zero if in range and valid
    if min_val <= 0 <= max_val:
        zero_val = round_to_multiple(0)
        if zero_val not in test_cases:
            test_cases.append(zero_val)

    # Add a negative value if allowed and not already present
    if min_val < 0 and max_val > 0:
        neg_val = (
            round_to_multiple(min_val / 2)
            if min_val > -1000
            else round_to_multiple(-100)
        )
        if neg_val not in test_cases and min_val <= neg_val <= max_val:
            test_cases.append(neg_val)

    # Ensure all test cases respect multipleOf
    test_cases = [int(ex) for ex in test_cases if ex % multiple_of == 0]

    return sorted(set(test_cases)), warning


def generate_number_test_cases(schema, field_name="field"):
    """Generate number (float) test cases from schema.

    Args:
        schema: OpenAPI schema for a number field
        field_name: Name of the field (for error messages)

    Returns:
        tuple: (list of test values, optional warning message)
    """
    test_cases = []
    warning = None

    # Check for enum
    if "enum" in schema:
        return schema["enum"], None

    # Get constraints
    minimum = schema.get("minimum")
    maximum = schema.get("maximum")
    exclusive_min = schema.get("exclusiveMinimum")
    exclusive_max = schema.get("exclusiveMaximum")
    multiple_of = schema.get("multipleOf")

    # Determine actual bounds
    if exclusive_min is not None:
        min_val = exclusive_min + 0.01
    elif minimum is not None:
        min_val = minimum
    else:
        min_val = -1000000.0
        warning = f"⚠️  Field '{field_name}': No minimum specified. Testing with very large negative numbers. Add 'minimum' to schema to restrict."

    if exclusive_max is not None:
        max_val = exclusive_max - 0.01
    elif maximum is not None:
        max_val = maximum
    else:
        max_val = 1000000.0
        if not warning:
            warning = f"⚠️  Field '{field_name}': No maximum specified. Testing with very large positive numbers. Add 'maximum' to schema to restrict."

    # Add boundary values
    test_cases.append(float(min_val))
    test_cases.append(float(max_val))

    # Add middle value
    mid_val = (min_val + max_val) / 2
    test_cases.append(mid_val)

    # Add zero if in range
    if min_val <= 0 <= max_val:
        if multiple_of:
            zero_val = 0.0 if 0.0 % multiple_of == 0 else multiple_of
            test_cases.append(zero_val)
        else:
            test_cases.append(0.0)

    # Add high-precision numbers
    if min_val < 1 < max_val:
        test_cases.extend([0.123456789, 0.999999999, 1.111111111])

    # Add negative if allowed
    if min_val < 0 < max_val:
        test_cases.append(-0.123456789)

    # Apply multipleOf constraint if specified
    if multiple_of:
        filtered = []
        for ex in test_cases:
            # Check if it's a valid multiple
            if abs((ex / multiple_of) - round(ex / multiple_of)) < 0.0001:
                filtered.append(ex)
        if filtered:
            test_cases = filtered
        else:
            # Generate some valid multiples
            test_cases = [
                multiple_of * i
                for i in range(
                    int(min_val / multiple_of), int(max_val / multiple_of) + 1
                )
                if min_val <= multiple_of * i <= max_val
            ][:5]

    # Filter to ensure within bounds
    test_cases = [ex for ex in test_cases if min_val <= ex <= max_val]

    return sorted(set(test_cases)), warning


def generate_boolean_test_cases(schema):
    """Generate boolean test cases.

    Args:
        schema: OpenAPI schema for a boolean field

    Returns:
        list: [True, False]
    """
    return [True, False]


def generate_array_test_cases(schema, field_name="field"):
    """Generate array test cases from schema.

    Args:
        schema: OpenAPI schema for an array field
        field_name: Name of the field (for error messages)

    Returns:
        tuple: (list of test arrays, optional warning message)
    """
    items_schema = schema.get("items", {})
    min_items = schema.get("minItems", 0)
    max_items = schema.get("maxItems", 3)

    # Generate test cases for the item type
    item_test_cases, warning = generate_test_cases_for_schema(
        items_schema, f"{field_name}[]"
    )

    arrays = []

    # Empty array if allowed
    if min_items == 0:
        arrays.append([])

    # Single item array if allowed
    if min_items <= 1 <= max_items and item_test_cases:
        arrays.append([item_test_cases[0]])

    # Min items array
    if min_items > 0 and item_test_cases:
        arrays.append(item_test_cases[:min_items])

    # Max items array
    if item_test_cases:
        arrays.append(item_test_cases[:max_items])

    return arrays, warning


def generate_object_test_cases(schema, field_name="field"):
    """Generate object test cases from schema.

    Args:
        schema: OpenAPI schema for an object field
        field_name: Name of the field (for error messages)

    Returns:
        tuple: (list of test objects, list of warnings)
    """
    properties = schema.get("properties", {})

    test_cases = []
    warnings = []

    # Generate one complete test case with all properties
    obj = {}
    for prop_name, prop_schema in properties.items():
        prop_test_cases, warning = generate_test_cases_for_schema(
            prop_schema, f"{field_name}.{prop_name}"
        )
        if warning:
            warnings.append(warning)
        if prop_test_cases:
            obj[prop_name] = prop_test_cases[0]

    test_cases.append(obj)

    return test_cases, warnings


def generate_test_cases_for_schema(schema, field_name="field"):
    """Generate test cases for any schema type.

    Args:
        schema: OpenAPI schema
        field_name: Name of the field (for error messages)

    Returns:
        tuple: (list of test values, optional warning message or list of warnings)
    """
    schema_type = schema.get("type", "string")

    if schema_type == "string":
        return generate_string_test_cases(schema), None
    elif schema_type == "integer":
        return generate_integer_test_cases(schema, field_name)
    elif schema_type == "number":
        return generate_number_test_cases(schema, field_name)
    elif schema_type == "boolean":
        return generate_boolean_test_cases(schema), None
    elif schema_type == "array":
        return generate_array_test_cases(schema, field_name)
    elif schema_type == "object":
        return generate_object_test_cases(schema, field_name)
    else:
        return ["test-value"], None
