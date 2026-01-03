## openapi.py

Responsible for validating the OpenAPI specification.

Key responsibilities:
- Ensure request bodies exist
- Ensure responses exist
- Ensure examples or schemas are present
- Ensure all schema fields have descriptions

This module fails fast before any HTTP calls are made.