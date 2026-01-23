"""Mock server with complete OpenAPI spec including all examples."""

from flask import Flask, jsonify, request

app = Flask(__name__)

# In-memory database
users_db = {}
next_id = 1


def reset_db():
    """Reset database to initial state."""
    global users_db, next_id
    users_db = {
        1: {"id": 1, "name": "Alice", "email": "alice@example.com"},
        2: {"id": 2, "name": "Bob", "email": "bob@example.com"},
    }
    next_id = 3


# Initialize on startup
reset_db()


@app.route("/openapi.json")
def openapi():
    """Return complete OpenAPI spec with all required examples."""
    return jsonify(
        {
            "openapi": "3.0.0",
            "info": {"title": "Valid Users API", "version": "1.0.0"},
            "paths": {
                "/users": {
                    "get": {
                        "summary": "Get all users",
                        "responses": {
                            "200": {
                                "description": "Successful response",
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "type": "array",
                                            "items": {
                                                "type": "object",
                                                "required": [
                                                    "id",
                                                    "name",
                                                    "email",
                                                ],
                                                "properties": {
                                                    "id": {
                                                        "type": "integer",
                                                        "description": "User ID",
                                                    },
                                                    "name": {
                                                        "type": "string",
                                                        "description": "User name",
                                                    },
                                                    "email": {
                                                        "type": "string",
                                                        "description": "User email",
                                                    },
                                                },
                                            },
                                        },
                                        "example": [
                                            {
                                                "id": 1,
                                                "name": "Alice",
                                                "email": "alice@example.com",
                                            },
                                            {
                                                "id": 2,
                                                "name": "Bob",
                                                "email": "bob@example.com",
                                            },
                                        ],
                                    }
                                },
                            }
                        },
                    },
                    "post": {
                        "summary": "Create a new user",
                        "requestBody": {
                            "required": True,
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "required": ["name", "email"],
                                        "properties": {
                                            "name": {
                                                "type": "string",
                                                "description": "User name",
                                            },
                                            "email": {
                                                "type": "string",
                                                "description": "User email",
                                            },
                                        },
                                    },
                                    "example": {
                                        "name": "Charlie",
                                        "email": "charlie@example.com",
                                    },
                                }
                            },
                        },
                        "responses": {
                            "201": {
                                "description": "User created",
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "type": "object",
                                            "properties": {
                                                "id": {
                                                    "type": "integer",
                                                    "description": "User ID",
                                                },
                                                "name": {
                                                    "type": "string",
                                                    "description": "User name",
                                                },
                                                "email": {
                                                    "type": "string",
                                                    "description": "User email",
                                                },
                                            },
                                        },
                                        "example": {
                                            "id": 3,
                                            "name": "Charlie",
                                            "email": "charlie@example.com",
                                        },
                                    }
                                },
                            },
                            "422": {
                                "description": "Validation error",
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
                                        "example": {
                                            "error": "Missing required field"
                                        },
                                    }
                                },
                            },
                        },
                    },
                },
                "/users/{user_id}": {
                    "put": {
                        "summary": "Update a user",
                        "parameters": [
                            {
                                "name": "user_id",
                                "in": "path",
                                "required": True,
                                "schema": {"type": "integer"},
                            }
                        ],
                        "requestBody": {
                            "required": True,
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "properties": {
                                            "name": {
                                                "type": "string",
                                                "description": "User name",
                                            },
                                            "email": {
                                                "type": "string",
                                                "description": "User email",
                                            },
                                        },
                                    },
                                    "example": {
                                        "name": "Alice Updated",
                                        "email": "alice.updated@example.com",
                                    },
                                }
                            },
                        },
                        "responses": {
                            "200": {
                                "description": "User updated",
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "type": "object",
                                            "properties": {
                                                "id": {
                                                    "type": "integer",
                                                    "description": "User ID",
                                                },
                                                "name": {
                                                    "type": "string",
                                                    "description": "User name",
                                                },
                                                "email": {
                                                    "type": "string",
                                                    "description": "User email",
                                                },
                                            },
                                        },
                                        "example": {
                                            "id": 1,
                                            "name": "Alice Updated",
                                            "email": "alice.updated@example.com",
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
                    "delete": {
                        "summary": "Delete a user",
                        "parameters": [
                            {
                                "name": "user_id",
                                "in": "path",
                                "required": True,
                                "schema": {"type": "integer"},
                            }
                        ],
                        "responses": {
                            "204": {
                                "description": "User deleted",
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
                },
            },
        }
    )


@app.route("/users", methods=["GET"])
def get_users():
    """Get all users."""
    return jsonify(list(users_db.values()))


@app.route("/reset", methods=["POST"])
def reset():
    """Reset database to initial state for testing."""
    reset_db()
    return jsonify({"status": "reset"}), 200


@app.route("/users", methods=["POST"])
def create_user():
    """Create a new user."""
    global next_id
    data = request.get_json()

    if not data or "name" not in data or "email" not in data:
        return jsonify({"error": "Missing required field"}), 422

    user = {"id": next_id, "name": data["name"], "email": data["email"]}
    users_db[next_id] = user
    next_id += 1

    return jsonify(user), 201


@app.route("/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    """Update a user."""
    if user_id not in users_db:
        return jsonify({"error": "User not found"}), 404

    data = request.get_json()
    user = users_db[user_id]

    if "name" in data:
        user["name"] = data["name"]
    if "email" in data:
        user["email"] = data["email"]

    return jsonify(user)


@app.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    """Delete a user."""
    if user_id not in users_db:
        return jsonify({"error": "User not found"}), 404

    del users_db[user_id]
    return "", 204


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
