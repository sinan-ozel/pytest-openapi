"""Mock server - validates UUID format in request body, returns descriptive 400."""

import re

from flask import Flask, jsonify, request

app = Flask(__name__)

_UUID_RE = re.compile(
    r"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$"
)


def _is_valid_uuid(value):
    if not isinstance(value, str):
        return False, "UUID must be a string"
    if not _UUID_RE.match(value):
        return (
            False,
            "UUID must follow the pattern xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx "
            "(8-4-4-4-12 hexadecimal characters separated by hyphens)",
        )
    return True, None


@app.route("/openapi.json")
def openapi():
    return jsonify(
        {
            "openapi": "3.0.0",
            "info": {"title": "Resource API", "version": "1.0.0"},
            "paths": {
                "/resource": {
                    "post": {
                        "summary": "Link to an existing resource by UUID",
                        "requestBody": {
                            "required": True,
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "required": ["resource_id", "label"],
                                        "properties": {
                                            "resource_id": {
                                                "type": "string",
                                                "format": "uuid",
                                                "description": "UUID of the target resource",
                                            },
                                            "label": {
                                                "type": "string",
                                                "description": "Human-readable label",
                                            },
                                        },
                                    },
                                    "example": {
                                        "resource_id": "550e8400-e29b-41d4-a716-446655440000",
                                        "label": "My resource",
                                    },
                                }
                            },
                        },
                        "responses": {
                            "200": {
                                "description": "Resource linked",
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "type": "object",
                                            "properties": {
                                                "id": {
                                                    "type": "integer",
                                                    "description": "Link ID",
                                                },
                                                "status": {
                                                    "type": "string",
                                                    "description": "Link status",
                                                },
                                            },
                                        },
                                        "example": {
                                            "id": 1,
                                            "status": "linked",
                                        },
                                    }
                                },
                            },
                            "400": {
                                "description": "Invalid UUID format",
                                "content": {
                                    "application/json": {
                                        "example": {
                                            "error": "Invalid UUID format",
                                            "field": "resource_id",
                                            "detail": "UUID must follow the pattern xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
                                        }
                                    }
                                },
                            },
                        },
                    }
                }
            },
        }
    )


_next_id = 1


@app.route("/resource", methods=["POST"])
def link_resource():
    global _next_id
    data = request.get_json(silent=True) or {}
    resource_id = data.get("resource_id", "")
    valid, reason = _is_valid_uuid(resource_id)
    if not valid:
        return (
            jsonify(
                {
                    "error": "Invalid UUID format",
                    "field": "resource_id",
                    "detail": reason,
                }
            ),
            400,
        )
    result = {"id": _next_id, "status": "linked"}
    _next_id += 1
    return jsonify(result), 200


@app.route("/reset", methods=["POST"])
def reset():
    global _next_id
    _next_id = 1
    return jsonify({"status": "reset"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
