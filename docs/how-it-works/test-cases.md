## Test Case Generation

Test cases are collected from:

1. Explicit `example`
2. Named `examples`
3. Generated values from `schema`

Schema-based generation allows testing even when examples
are incomplete or missing.

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