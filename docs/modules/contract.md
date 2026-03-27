## contract.py

Executes contract tests against a live API.

Includes:
- HTTP request execution
- GET / POST / PUT / DELETE test logic
- Path parameter substitution (`substitute_path_params`) for all HTTP methods
- Schema-based request/response comparison
- Centralized test result logging

## schema.py

Handles OpenAPI schema resolution for both 3.0.x and 3.1.x specs.

Includes:
- `resolve_ref`: follows `$ref` JSON Pointer strings within the spec document
- `resolve_schema`: fully resolves a schema by following `$ref` pointers (with sibling keyword merging) and flattening `allOf` compositions
- `primary_type`: extracts the primary non-null type from a multi-type array (`type: ["string", "null"]`)