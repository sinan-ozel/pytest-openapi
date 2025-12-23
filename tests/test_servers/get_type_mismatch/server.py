"""Mock server - GET endpoint with type mismatch in response."""

from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/openapi.json")
def openapi():
    """OpenAPI spec with integer ID in example."""
    return jsonify(
        {
            "openapi": "3.0.0",
            "info": {"title": "GET Type Mismatch API", "version": "1.0.0"},
            "paths": {
                "/item": {
                    "get": {
                        "summary": "Get item",
                        "responses": {
                            "200": {
                                "description": "Successful response",
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "type": "object",
                                            "properties": {
                                                "id": {
                                                    "type": "integer",
                                                    "description": "Item ID"
                                                },
                                                "name": {
                                                    "type": "string",
                                                    "description": "Item name"
                                                },
                                            },
                                        },
                                        "example": {"id": 1, "name": "Item"},
                                    }
                                },
                            }
                        },
                    }
                }
            },
        }
    )


@app.route("/item")
def get_item():
    """Get item - id is STRING instead of INTEGER."""
    return jsonify({"id": "1", "name": "Item"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
