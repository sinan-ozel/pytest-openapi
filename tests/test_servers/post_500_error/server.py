"""Mock server - POST endpoint returning 500 instead of 200."""

from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route("/openapi.json")
def openapi():
    """OpenAPI spec expecting 200 response."""
    return jsonify(
        {
            "openapi": "3.0.0",
            "info": {"title": "POST 500 Error API", "version": "1.0.0"},
            "paths": {
                "/order": {
                    "post": {
                        "summary": "Create order",
                        "requestBody": {
                            "required": True,
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "properties": {
                                            "item": {
                                                "type": "string",
                                                "description": "Item name",
                                            }
                                        },
                                    },
                                    "example": {"item": "Widget"},
                                }
                            },
                        },
                        "responses": {
                            "200": {
                                "description": "Order created",
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "type": "object",
                                            "properties": {
                                                "id": {
                                                    "type": "integer",
                                                    "description": "Order ID",
                                                }
                                            },
                                        },
                                        "example": {"id": 1},
                                    }
                                },
                            }
                        },
                    }
                }
            },
        }
    )


@app.route("/order", methods=["POST"])
def create_order():
    """Create order - RETURNS 500 ERROR."""
    return jsonify({"error": "Internal server error"}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
