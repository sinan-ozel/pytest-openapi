## OpenAPI Quality Enforcement

The tool enforces the following rules:

- Every request body must define:
  - an example OR a schema
- Every response must define:
  - an example OR a schema
- Every schema field must include a `description`

These rules ensure the spec is:
- testable
- self-documenting
- suitable for automation