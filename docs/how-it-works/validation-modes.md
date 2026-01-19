# Validation Modes

pytest-openapi supports two validation strategies depending on the test case origin and user preferences.

## Hybrid Validation Approach

The tool uses a **hybrid validation approach** that distinguishes between example-based tests and schema-generated tests:

### Example-Based Tests

When your OpenAPI spec includes explicit request/response examples, pytest-openapi tests these examples against your live API.

**Default Behavior (Strict Mode)**:
- Request example → Response must match example exactly
- Validates structure, types, and **exact values**
- Array lengths must match
- All field values must match

**Example**:
```yaml
responses:
  200:
    content:
      application/json:
        example:
          context: [1, 2, 3]
          total_duration: 1000000000
```

In strict mode, the actual response must have exactly 3 elements in `context` and `total_duration` must be exactly `1000000000`.

### Schema-Generated Tests

When pytest-openapi generates test cases from your schema (not from examples), it **always uses schema validation**:

- Validates structure and types only
- Does not enforce specific values
- Array lengths are flexible (any length is valid)
- Only checks that elements match the schema type

This allows broad coverage testing of different input combinations.

## Lenient Mode for Examples

Sometimes examples contain **placeholder values** that don't match actual API responses:

```yaml
example:
  context: [1, 2, 3]  # Placeholder data
  response: "The capital of France is Paris."
```

But your actual API might return:
```json
{
  "context": [],  # Empty in real implementation
  "response": "The capital of France is Paris."
}
```

### Using `--openapi-no-strict-example-checking`

Add this flag to use **lenient validation** for example-based tests:

```bash
pytest --openapi=http://localhost:8000 --openapi-no-strict-example-checking
```

**Lenient mode validates**:
- ✅ All expected keys are present
- ✅ Types match (string, number, array, object, etc.)
- ✅ Nested structure matches
- ✅ Array element types match
- ❌ Exact values (ignored)
- ❌ Array lengths (ignored)

## When to Use Each Mode

### Use Strict Mode (Default) When:
- Your examples accurately reflect real API behavior
- You want to ensure examples stay synchronized with implementation
- You're testing documented example interactions

### Use Lenient Mode When:
- Examples contain placeholder or sample data
- Array lengths vary in real responses
- Dynamic values (timestamps, IDs) differ per request
- You want structural validation without exact value matching

## Validation Decision Matrix

| Test Case Origin | Example Present? | Strict Flag | Validation Type |
|-----------------|------------------|-------------|-----------------|
| Example-based | Yes | Default (strict) | Exact value matching |
| Example-based | Yes | `--no-strict...` | Structure/type only |
| Schema-generated | Any | Any | Schema validation (always) |

## Philosophy

pytest-openapi is **opinionated**: 

- Examples are **required** in your OpenAPI spec
- This ensures documentation is complete and useful
- Generated tests provide broad coverage
- Example tests ensure documented interactions work

The hybrid approach gives you:
1. **Confidence** that your examples are accurate (strict mode)
2. **Flexibility** when examples are illustrative (lenient mode)
3. **Coverage** through schema-generated test cases
