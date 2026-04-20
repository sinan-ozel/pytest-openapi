## Test Case Generation

Test cases are collected from:

1. Explicit `example`
2. Named `examples`
3. Generated values from `schema`

Schema-based generation allows testing even when examples
are incomplete or missing.

### Schema Resolution

Before generating test cases, schemas are fully resolved:

- **`$ref` pointers** are followed and their target schemas are inlined. In OpenAPI 3.1.x, sibling keywords next to a `$ref` are merged in (overriding the referenced schema where they conflict).
- **`allOf` schemas** are merged: properties and `required` lists from every sub-schema are combined into a single flat schema before generation.
- **Nullable types** (`type: ["string", "null"]` in OpenAPI 3.1.x) are handled by extracting the primary non-null type for generation purposes.

### Object Test Cases

For object schemas, pytest-openapi generates test cases by taking the Cartesian product of valid values for each property. Only valid enum values are included in these combinations to avoid generating request bodies that would be rejected by the server.

In addition to the valid combinations, one extra object is generated for every string property annotated with a recognised format (see below). That extra object replaces only the format-constrained field with a deliberately invalid value while keeping all other fields valid. This produces a negative test case that must trigger a 400 or 422 from the server.

### Format-Based Negative Tests

When an OpenAPI schema marks a string property with one of the following formats, pytest-openapi generates an invalid value and expects the server to return **400 Bad Request** or **422 Unprocessable Entity** with a **non-empty, human-readable error message** in the response body.

| Format | Example valid value | Example invalid value used |
|---|---|---|
| `email` | `test@example.com` | `not-an-email` |
| `uri` / `url` | `https://example.com/path` | `not-a-uri` |
| `ipv4` / `ip` | `192.168.1.1` | `999.999.999.999` |
| `ipv6` | `2001:db8::1` | `gggg::1` |
| `hostname` / `idn-hostname` | `api.example.com` | `-invalid.start.com` |
| `uuid` | `550e8400-e29b-41d4-a716-446655440000` | `not-a-uuid` |

Formats intentionally excluded: `date`, `date-time`, `time` (server-side validation for these is inconsistent and out of scope).

#### Error message requirement

When the server returns 400 or 422 for an invalid-format value, the response body must contain at least one non-whitespace string. An empty body (`{}`) causes the test to **fail**. The plugin does not check for any specific word — it only verifies that a human-readable explanation is present.

## Validation Strategy

pytest-openapi uses different validation approaches depending on the test case origin:

- **Example-based tests**: Validated against the example (strict or lenient mode)
- **Schema-generated tests**: Always validated against the JSON schema

See [Validation Modes](validation-modes.md) for detailed information about strict vs. lenient validation.

## Opinionated Requirements

pytest-openapi requires:

- Examples must be present in your OpenAPI spec
- Responses must include examples (not just schemas)
- This ensures documentation is complete and useful for consumers