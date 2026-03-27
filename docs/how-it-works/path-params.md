## Path Parameter Resolution

Before making a request, pytest-openapi substitutes OpenAPI path parameter placeholders with concrete values.

### GET and DELETE endpoints

Path parameters are replaced with type-appropriate defaults derived from the parameter's schema:

| Parameter type | Default value |
|---------------|---------------|
| `integer`     | `1`           |
| `number`      | `1.0`         |
| `boolean`     | `true`        |
| `string`      | `test`        |

Example: `/users/{userId}` (userId is `integer`) → `/users/1`

### POST and PUT endpoints

Path parameters are resolved using:
- Response examples (`id`, `*_id` fields)
- Schema-generated values
- Fallback defaults (same table as above)

Example:
`/users/{user_id}` → `/users/1`