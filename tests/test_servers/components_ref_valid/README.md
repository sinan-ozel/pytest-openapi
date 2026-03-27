# components_ref_valid

Mock server for a **Bookstore Catalog API** using OpenAPI 3.1.0 `components/schemas` with `$ref` references.

## Purpose

Stress-tests the plugin's ability to resolve `$ref` pointers to `components/schemas` when validating responses. All responses are correct and this server **should PASS** validation.

## Schema Features

- `components/schemas`: `Author`, `Book`, `NewBook`
- `$ref: "#/components/schemas/Book"` used in response schemas
- Nested `$ref`: `Book.author` references `#/components/schemas/Author`
- `$ref` on request body schema (`NewBook`)
- OpenAPI version `3.1.0`

## Endpoints

### GET /catalog/books
Returns a list of books. Response schema uses `$ref` to `Book`, which itself contains a nested `$ref` to `Author`.

**Example response:**
```json
[
  {
    "id": 1,
    "title": "The Pragmatic Programmer",
    "isbn": "978-0135957059",
    "year": 2019,
    "price": 49.99,
    "author": { "id": 1, "name": "David Thomas", "bio": "..." }
  }
]
```

### POST /catalog/books
Creates a new book. Request schema uses `$ref` to `NewBook`; response schema uses `$ref` to `Book`.

**Example request:**
```json
{ "title": "Design Patterns", "isbn": "978-0201633610", "year": 1994, "price": 54.99, "author_id": 1 }
```

## Expected Test Outcome

**PASS** — All responses match the resolved schemas.
