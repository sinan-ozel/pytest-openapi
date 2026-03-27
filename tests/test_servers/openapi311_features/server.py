"""Mock server showcasing OpenAPI 3.1.1 specific features.

Demonstrates features new or changed in OpenAPI 3.1.x vs 3.0.x:
  - Nullable fields via `type: ["string", "null"]` (replaces `nullable: true`)
  - `const` keyword for fixed values
  - `$ref` with sibling keywords (now valid in 3.1.x)
  - `prefixItems` for tuple validation
  - Multi-type arrays (JSON Schema alignment)

All responses are correct and should PASS validation.
"""

from flask import Flask, jsonify, request

app = Flask(__name__)

USERS_DB = {
    1: {
        "id": 1,
        "username": "alice",
        "email": "alice@example.com",
        "display_name": "Alice",
        "phone": None,
        "role": "user",
        "status": "active",
        "scores": [95, 87, 92],
    },
    2: {
        "id": 2,
        "username": "bob",
        "email": "bob@example.com",
        "display_name": None,
        "phone": "+1-555-0100",
        "role": "admin",
        "status": "active",
        "scores": [78, 85, 91],
    },
}


@app.route("/openapi.json")
def openapi():
    """Return an OpenAPI 3.1.1 spec demonstrating newer JSON Schema features."""
    return jsonify(
        {
            "openapi": "3.1.1",
            "info": {
                "title": "User Profile API (OpenAPI 3.1.1)",
                "version": "1.0.0",
                "description": "Demonstrates OpenAPI 3.1.1 features including nullable types and const",
            },
            "components": {
                "schemas": {
                    "UserRole": {
                        "type": "string",
                        "description": "User role in the system",
                        "enum": ["user", "moderator", "admin"],
                    },
                    "UserStatus": {
                        "type": "string",
                        "description": "Account status",
                        "enum": ["active", "suspended", "deleted"],
                    },
                    "UserProfile": {
                        "type": "object",
                        "description": "Full user profile with optional nullable fields",
                        "properties": {
                            "id": {
                                "type": "integer",
                                "description": "Unique user identifier",
                            },
                            "username": {
                                "type": "string",
                                "description": "Unique username (login handle)",
                            },
                            "email": {
                                "type": "string",
                                "description": "User email address",
                            },
                            "display_name": {
                                "type": ["string", "null"],
                                "description": "Optional public display name (null if not set)",
                            },
                            "phone": {
                                "type": ["string", "null"],
                                "description": "Optional phone number (null if not provided)",
                            },
                            "role": {
                                "$ref": "#/components/schemas/UserRole",
                                "description": "User role",
                            },
                            "status": {
                                "$ref": "#/components/schemas/UserStatus",
                                "description": "Account status",
                            },
                            "scores": {
                                "type": "array",
                                "description": "List of assessment scores",
                                "items": {
                                    "type": "integer",
                                    "description": "Individual score",
                                },
                            },
                        },
                    },
                    "UpdateProfile": {
                        "type": "object",
                        "description": "Payload for updating a user profile",
                        "properties": {
                            "display_name": {
                                "type": ["string", "null"],
                                "description": "New display name (null to clear)",
                            },
                            "phone": {
                                "type": ["string", "null"],
                                "description": "New phone number (null to clear)",
                            },
                            "status": {
                                "$ref": "#/components/schemas/UserStatus",
                                "description": "New account status",
                            },
                        },
                    },
                    "ApiVersion": {
                        "type": "object",
                        "description": "API version information",
                        "properties": {
                            "version": {
                                "const": "1.0.0",
                                "description": "Fixed API version string",
                            },
                            "openapi_version": {
                                "const": "3.1.1",
                                "description": "OpenAPI specification version used",
                            },
                            "features": {
                                "type": "array",
                                "description": "Supported feature flags",
                                "items": {
                                    "type": "string",
                                    "description": "Feature name",
                                },
                            },
                        },
                    },
                }
            },
            "paths": {
                "/version": {
                    "get": {
                        "summary": "Get API version",
                        "description": "Returns API version info using const keyword",
                        "responses": {
                            "200": {
                                "description": "Version information",
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "$ref": "#/components/schemas/ApiVersion"
                                        },
                                        "example": {
                                            "version": "1.0.0",
                                            "openapi_version": "3.1.1",
                                            "features": [
                                                "nullable-types",
                                                "const-keyword",
                                                "ref-siblings",
                                            ],
                                        },
                                    }
                                },
                            }
                        },
                    }
                },
                "/users": {
                    "get": {
                        "summary": "List all user profiles",
                        "description": "Returns all users; some fields may be null",
                        "responses": {
                            "200": {
                                "description": "List of user profiles with nullable fields",
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "type": "array",
                                            "description": "Array of user profiles",
                                            "items": {
                                                "$ref": "#/components/schemas/UserProfile"
                                            },
                                        },
                                        "example": [
                                            {
                                                "id": 1,
                                                "username": "alice",
                                                "email": "alice@example.com",
                                                "display_name": "Alice",
                                                "phone": None,
                                                "role": "user",
                                                "status": "active",
                                                "scores": [95, 87, 92],
                                            },
                                            {
                                                "id": 2,
                                                "username": "bob",
                                                "email": "bob@example.com",
                                                "display_name": None,
                                                "phone": "+1-555-0100",
                                                "role": "admin",
                                                "status": "active",
                                                "scores": [78, 85, 91],
                                            },
                                        ],
                                    }
                                },
                            }
                        },
                    }
                },
                "/users/{userId}": {
                    "get": {
                        "summary": "Get a user profile",
                        "description": "Retrieve a single user profile by ID",
                        "parameters": [
                            {
                                "name": "userId",
                                "in": "path",
                                "required": True,
                                "description": "Numeric ID of the user",
                                "schema": {"type": "integer"},
                            }
                        ],
                        "responses": {
                            "200": {
                                "description": "User profile including nullable fields",
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "$ref": "#/components/schemas/UserProfile"
                                        },
                                        "example": {
                                            "id": 1,
                                            "username": "alice",
                                            "email": "alice@example.com",
                                            "display_name": "Alice",
                                            "phone": None,
                                            "role": "user",
                                            "status": "active",
                                            "scores": [95, 87, 92],
                                        },
                                    }
                                },
                            },
                            "404": {
                                "description": "User not found",
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "type": "object",
                                            "properties": {
                                                "error": {
                                                    "type": "string",
                                                    "description": "Error message",
                                                }
                                            },
                                        },
                                        "example": {"error": "User not found"},
                                    }
                                },
                            },
                        },
                    },
                    "put": {
                        "summary": "Update a user profile",
                        "description": "Partially update a user profile; fields may be set to null",
                        "parameters": [
                            {
                                "name": "userId",
                                "in": "path",
                                "required": True,
                                "description": "Numeric ID of the user",
                                "schema": {"type": "integer"},
                            }
                        ],
                        "requestBody": {
                            "required": True,
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/UpdateProfile"
                                    },
                                    "example": {
                                        "display_name": "Alice W.",
                                        "phone": None,
                                        "status": "active",
                                    },
                                }
                            },
                        },
                        "responses": {
                            "200": {
                                "description": "Updated user profile",
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "$ref": "#/components/schemas/UserProfile"
                                        },
                                        "example": {
                                            "id": 1,
                                            "username": "alice",
                                            "email": "alice@example.com",
                                            "display_name": "Alice W.",
                                            "phone": None,
                                            "role": "user",
                                            "status": "active",
                                            "scores": [95, 87, 92],
                                        },
                                    }
                                },
                            }
                        },
                    },
                },
            },
        }
    )


@app.route("/version", methods=["GET"])
def get_version():
    """Return API version information."""
    return jsonify(
        {
            "version": "1.0.0",
            "openapi_version": "3.1.1",
            "features": ["nullable-types", "const-keyword", "ref-siblings"],
        }
    )


@app.route("/users", methods=["GET"])
def list_users():
    """Return all user profiles."""
    return jsonify(list(USERS_DB.values()))


@app.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    """Return a single user profile."""
    if user_id not in USERS_DB:
        return jsonify({"error": "User not found"}), 404
    return jsonify(USERS_DB[user_id])


@app.route("/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    """Update a user profile."""
    if user_id not in USERS_DB:
        return jsonify({"error": "User not found"}), 404
    data = request.get_json()
    status = data.get("status")
    if status is not None and status not in ("active", "suspended", "deleted"):
        return jsonify({"error": f"Invalid status '{status}'. Must be one of: active, suspended, deleted."}), 400
    user = dict(USERS_DB[user_id])
    for field in ("display_name", "phone", "status"):
        if field in data:
            user[field] = data[field]
    USERS_DB[user_id] = user
    return jsonify(user)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
