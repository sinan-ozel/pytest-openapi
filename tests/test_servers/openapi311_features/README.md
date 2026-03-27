# openapi311_features

Mock server showcasing **OpenAPI 3.1.1 specific features** for a User Profile API.

## Purpose

Stress-tests the plugin against features that are new or changed in OpenAPI 3.1.x compared to 3.0.x. All responses are correct and this server **should PASS** validation.

## OpenAPI 3.1.1 Features Demonstrated

| Feature | Where used |
|---------|-----------|
| `type: ["string", "null"]` | `display_name`, `phone` fields (nullable) |
| `const` keyword | `version` and `openapi_version` in `ApiVersion` schema |
| `$ref` with sibling keywords | `role` and `status` fields carry both `$ref` and `description` |
| Nested `$ref` chains | `UserProfile.role` → `UserRole`; `UserProfile.status` → `UserStatus` |
| `openapi: "3.1.1"` | Top-level version field |

## Key Schema Differences from OpenAPI 3.0.x

- **Nullable**: `3.0.x` used `nullable: true`. `3.1.x` uses `type: ["string", "null"]` (full JSON Schema alignment).
- **`const`**: New in 3.1.x (from JSON Schema). Validates a field has exactly one fixed value.
- **`$ref` siblings**: In `3.0.x`, sibling keywords next to `$ref` were ignored. In `3.1.x` they are merged.

## Endpoints

### GET /version
Returns API version info. Uses `const` to assert fixed string values.

### GET /users
Returns all user profiles. Some users have `null` values for `display_name` or `phone`.

### GET /users/{userId}
Returns a single user. Nullable fields may be `null`.

### PUT /users/{userId}
Updates a user profile. Request and response use schemas with `type: ["string", "null"]`.

## Expected Test Outcome

**PASS** — All responses match the 3.1.1 schemas.
