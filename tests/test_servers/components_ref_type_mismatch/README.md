# components_ref_type_mismatch

Mock server using the same **Bookstore Catalog API** spec as `components_ref_valid`, but intentionally returning `year` as a `string` instead of an `integer`.

## Purpose

Tests that the plugin detects type mismatches in responses even when the schema is defined via `$ref` to `components/schemas`. This server **should FAIL** validation.

## The Bug

The `Book` schema (referenced via `$ref`) declares:
```json
"year": { "type": "integer", "description": "Publication year" }
```

But the server returns:
```json
{ "year": "2019" }
```

## Schema Features

- Same `components/schemas` structure as `components_ref_valid`
- `$ref` used throughout — requires the plugin to dereference `$ref` to detect the type error
- OpenAPI version `3.1.0`

## Endpoints

### GET /catalog/books
Returns books with `year` as a string (bug).

### POST /catalog/books
Returns the created book with `year` as a string (bug).

## Expected Test Outcome

**FAIL** — Type mismatch: `year` is `string` but schema (via `$ref`) says `integer`.
