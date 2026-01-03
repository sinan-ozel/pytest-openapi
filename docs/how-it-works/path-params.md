## Path Parameter Resolution

Path parameters are resolved using:
- Response examples (`id`, `*_id`)
- Schema-generated values
- Fallback defaults

Example:
`/users/{user_id}` → `/users/1`