"""Mock server that returns invalid enum values to test enum validation."""

from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route("/openapi.json")
def openapi():
    """Return OpenAPI spec with enum in response schema."""
    return jsonify(
        {
            "openapi": "3.0.0",
            "info": {"title": "Enum Validation Test API", "version": "1.0.0"},
            "paths": {
                "/status": {
                    "get": {
                        "summary": "Get status with enum field",
                        "responses": {
                            "200": {
                                "description": "Status response",
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "type": "object",
                                            "properties": {
                                                "status": {
                                                    "type": "string",
                                                    "enum": ["active", "inactive", "pending"],
                                                    "description": "Status enum field",
                                                },
                                                "code": {
                                                    "type": "integer",
                                                    "description": "Status code",
                                                },
                                            },
                                            "required": ["status", "code"],
                                        },
                                        "example": {
                                            "status": "active",
                                            "code": 200,
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


@app.route("/status", methods=["GET"])
def get_status():
    """Return a response with INVALID enum value."""
    # This should fail enum validation because "invalid_status" is not in the enum
    return jsonify({"status": "invalid_status", "code": 200}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
