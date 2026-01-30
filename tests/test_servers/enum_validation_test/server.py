"""Mock server that validates enum values in requests."""

from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route("/openapi.json")
def openapi():
    """Return OpenAPI spec with enum in request and response schema."""
    return jsonify(
        {
            "openapi": "3.0.0",
            "info": {"title": "Enum Validation Test API", "version": "1.0.0"},
            "paths": {
                "/status": {
                    "post": {
                        "summary": "Create status with enum field",
                        "requestBody": {
                            "required": True,
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
                                            "name": {
                                                "type": "string",
                                                "description": "Name field",
                                            },
                                        },
                                        "required": ["status", "name"],
                                    },
                                    "example": {
                                        "status": "active",
                                        "name": "Test Item",
                                    },
                                }
                            },
                        },
                        "responses": {
                            "200": {
                                "description": "Success",
                                "content": {
                                    "application/json": {
                                        "example": {
                                            "id": 123,
                                            "status": "created",
                                        }
                                    }
                                },
                            },
                            "400": {
                                "description": "Bad Request - Invalid enum value",
                                "content": {
                                    "application/json": {
                                        "example": {
                                            "error": "Invalid enum value",
                                            "field": "status",
                                            "value": "invalid_status",
                                            "allowed_values": ["active", "inactive", "pending"],
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


@app.route("/status", methods=["POST"])
def create_status():
    """Validate request enum and return success or error."""
    data = request.get_json()

    # Validate status field
    if "status" in data:
        valid_options = ["active", "inactive", "pending"]
        if data["status"] not in valid_options:
            return jsonify({
                "error": "Invalid enum value",
                "field": "status",
                "value": data["status"],
                "allowed_values": valid_options
            }), 400

    return jsonify({"id": 123, "status": "created"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
