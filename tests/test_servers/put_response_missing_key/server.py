"""Mock server - PUT response missing key."""

from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route("/openapi.json")
def openapi():
    """OpenAPI spec with complete response example."""
    return jsonify(
        {
            "openapi": "3.0.0",
            "info": {
                "title": "PUT Response Missing Key API",
                "version": "1.0.0",
            },
            "paths": {
                "/items/{item_id}": {
                    "put": {
                        "summary": "Update item",
                        "parameters": [
                            {
                                "name": "item_id",
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
                                                "description": "Item name",
                                            }
                                        },
                                    },
                                    "example": {"name": "Updated Item"},
                                }
                            },
                        },
                        "responses": {
                            "200": {
                                "description": "Item updated",
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "type": "object",
                                            "properties": {
                                                "id": {
                                                    "type": "integer",
                                                    "description": "Item ID",
                                                },
                                                "name": {
                                                    "type": "string",
                                                    "description": "Item name",
                                                },
                                                "updated": {
                                                    "type": "boolean",
                                                    "description": "Update status",
                                                },
                                            },
                                        },
                                        "example": {
                                            "id": 1,
                                            "name": "Updated Item",
                                            "updated": True,
                                        },
                                    }
                                },
                            }
                        },
                    }
                }
            },
        }
    )


@app.route("/items/<int:item_id>", methods=["PUT"])
def update_item(item_id):
    """Update item - MISSING 'updated' key in response."""
    data = request.get_json()
    return jsonify({"id": item_id, "name": data.get("name")})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
