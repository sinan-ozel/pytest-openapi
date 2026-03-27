"""Schema resolution for OpenAPI $ref, allOf, and multi-type support.

Bridges the gap between OpenAPI 3.0.x and 3.1.x:
- 3.1.x aligns with JSON Schema draft 2020-12
- $ref siblings are valid in 3.1.x (ignored in 3.0.x)
- Nullable uses type: ["string", "null"] instead of nullable: true
"""


def resolve_ref(spec, ref_string):
    """Follow a JSON Pointer $ref to its schema within the spec
    document.

    Only local references starting with '#/' are supported.

    Args:
        spec: Complete OpenAPI spec dict
        ref_string: A $ref value such as '#/components/schemas/Book'

    Returns:
        The referenced schema dict, or an empty dict if unresolvable
    """
    if not isinstance(ref_string, str) or not ref_string.startswith("#/"):
        return {}
    parts = ref_string[2:].split("/")
    node = spec
    for part in parts:
        if not isinstance(node, dict) or part not in node:
            return {}
        node = node[part]
    return node if isinstance(node, dict) else {}


def resolve_schema(spec, schema, _visited=None):
    """Return a fully resolved schema with $ref followed and allOf
    merged.

    Handles:
    - ``$ref``: recursively follows the reference and merges any sibling
      keywords (the merge semantics required by OpenAPI 3.1.x).
    - ``allOf``: merges ``properties`` and ``required`` lists from every
      sub-schema into a single flat schema.

    Neither ``oneOf`` nor ``anyOf`` is merged here; those require runtime
    data to choose the matching branch and are handled in the validator.

    Args:
        spec: Complete OpenAPI spec dict (needed to resolve $ref pointers)
        schema: Schema object to resolve
        _visited: Frozenset of $ref strings already on the resolution stack
                  (used to break cycles)

    Returns:
        Resolved schema dict.  Returns *schema* unchanged when *spec* is
        ``None`` or *schema* is not a dict.
    """
    if not isinstance(schema, dict) or not spec:
        return schema

    if _visited is None:
        _visited = frozenset()

    # ── $ref resolution ──────────────────────────────────────────────────────
    if "$ref" in schema:
        ref_string = schema["$ref"]
        if ref_string in _visited:
            # Cycle: return any sibling keywords without the $ref
            return {k: v for k, v in schema.items() if k != "$ref"}
        ref_schema = resolve_ref(spec, ref_string)
        if not ref_schema:
            return {k: v for k, v in schema.items() if k != "$ref"}
        new_visited = _visited | {ref_string}
        siblings = {k: v for k, v in schema.items() if k != "$ref"}
        resolved_ref = resolve_schema(spec, ref_schema, new_visited)
        if siblings:
            # Sibling keywords override values from the referenced schema
            return resolve_schema(
                spec, {**resolved_ref, **siblings}, new_visited
            )
        return resolved_ref

    # ── allOf merging ─────────────────────────────────────────────────────────
    if "allOf" in schema:
        # Start with outer keys (excluding 'allOf') as the base
        outer = {k: v for k, v in schema.items() if k != "allOf"}
        merged_props: dict = {}
        merged_required: list = []

        for sub in schema["allOf"]:
            resolved_sub = resolve_schema(spec, sub, _visited)
            merged_props.update(resolved_sub.get("properties", {}))
            merged_required.extend(resolved_sub.get("required", []))
            # Promote top-level fields (type, description…) not yet set
            for key, val in resolved_sub.items():
                if key not in ("properties", "required") and key not in outer:
                    outer[key] = val

        # Outer-level declarations win over what came from sub-schemas
        if "properties" in outer:
            merged_props.update(outer.pop("properties"))
        if "required" in outer:
            merged_required = list(set(outer.pop("required") + merged_required))

        result = dict(outer)
        if merged_props:
            result["properties"] = merged_props
        if merged_required:
            result["required"] = list(set(merged_required))
        return result

    return schema


def primary_type(schema_type):
    """Return the primary non-null type from a type field.

    In OpenAPI 3.1.x a type field may be a list, e.g. ``["string", "null"]``.
    This helper returns the first non-null entry, or the original value if it
    is already a plain string.

    Args:
        schema_type: The value of a schema's ``type`` field

    Returns:
        A single type string, or ``None`` if the input is ``None``
    """
    if isinstance(schema_type, list):
        non_null = [t for t in schema_type if t != "null"]
        return non_null[0] if non_null else None
    return schema_type
