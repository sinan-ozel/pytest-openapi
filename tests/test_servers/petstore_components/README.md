# petstore_components

Mock server implementing a simplified **Petstore API** based on the classic OpenAPI Petstore example spec, adapted for OpenAPI 3.1.0 with full use of `components/schemas`.

## Purpose

Provides a well-known, real-world-style API with components, `$ref`, path parameters, and multiple HTTP methods. All responses are correct and this server **should PASS** validation.

This is based on the canonical Petstore spec from https://petstore3.swagger.io (OpenAPI 3.x version).

## Schema Features

- `components/schemas`: `Pet`, `NewPet`, `Error`
- `$ref` used in all response and request body schemas
- Path parameters (`/pets/{petId}`)
- `enum` on `status` field (`"available"`, `"pending"`, `"adopted"`)
- Multiple HTTP methods: GET, POST, DELETE
- Multiple documented response codes (200, 201, 204, 404)
- OpenAPI version `3.1.0`

## Endpoints

### GET /pets
Returns a list of all pets using `$ref` to `Pet` schema.

### POST /pets
Creates a new pet. Request uses `NewPet` schema; response uses `Pet` schema.

### GET /pets/{petId}
Returns a single pet by ID. Responds 200 (Pet) or 404 (Error).

### DELETE /pets/{petId}
Deletes a pet by ID. Responds 204 (no content) or 404 (Error).

## Expected Test Outcome

**PASS** — All responses match the Petstore schemas.
