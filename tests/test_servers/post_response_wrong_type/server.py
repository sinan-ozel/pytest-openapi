"""Mock server - POST response with wrong type for a field."""

from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route("/openapi.json")
def openapi():
    """OpenAPI spec with integer ID in example."""
    return jsonify(
        {
            "openapi": "3.0.0",
            "info": {
                "title": "POST Response Wrong Type API",
                "version": "1.0.0",
            },
            "paths": {
                "/comment": {
                    "post": {
                        "summary": "Create comment",
                        "requestBody": {
                            "required": True,
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "properties": {
                                            "text": {"type": "string"}
                                        },
                                    },
                                    "example": {"text": "Great post!"},
                                }
                            },
                        },
                        "responses": {
                            "201": {
                                "description": "Comment created",
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "type": "object",
                                            "properties": {
                                                "id": {"type": "integer"},
                                                "text": {"type": "string"},
                                            },
                                        },
                                        "example": {
                                            "id": 1,
                                            "text": "Great post!",
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


@app.route("/comment", methods=["POST"])
def create_comment():
    """Create comment - id is STRING instead of INTEGER."""
    data = request.get_json()
    return jsonify({"id": "1", "text": data.get("text")}), 201


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
