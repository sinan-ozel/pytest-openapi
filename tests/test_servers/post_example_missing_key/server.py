"""Mock server - POST response has key that example doesn't have."""

from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route("/openapi.json")
def openapi():
    """OpenAPI spec with incomplete response example."""
    return jsonify(
        {
            "openapi": "3.0.0",
            "info": {
                "title": "POST Example Missing Key API",
                "version": "1.0.0",
            },
            "paths": {
                "/note": {
                    "post": {
                        "summary": "Create note",
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
                                    "example": {"text": "Meeting notes"},
                                }
                            },
                        },
                        "responses": {
                            "201": {
                                "description": "Note created",
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
                                            "text": "Meeting notes"
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


@app.route("/note", methods=["POST"])
def create_note():
    """Create note - response has EXTRA 'created_at' key."""
    data = request.get_json()
    return (
        jsonify(
            {"id": 1, "text": data.get("text"), "created_at": "2025-12-23"}
        ),
        201,
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
