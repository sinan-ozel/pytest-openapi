"""Mock server with nested schemas but missing some descriptions."""

from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route("/openapi.json")
def openapi():
    """Return OpenAPI spec with nested schemas but missing descriptions."""
    return jsonify(
        {
            "openapi": "3.0.0",
            "info": {"title": "Missing Descriptions API", "version": "1.0.0"},
            "paths": {
                "/orders": {
                    "post": {
                        "summary": "Create a new order",
                        "requestBody": {
                            "required": True,
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "properties": {
                                            "customer": {
                                                "type": "object",
                                                "description": "Customer information",
                                                "properties": {
                                                    "name": {
                                                        "type": "string",
                                                        "description": "Customer full name",
                                                    },
                                                    "email": {
                                                        "type": "string",
                                                        # MISSING DESCRIPTION HERE
                                                    },
                                                    "address": {
                                                        "type": "object",
                                                        "description": "Shipping address",
                                                        "properties": {
                                                            "street": {
                                                                "type": "string",
                                                                "description": "Street address",
                                                            },
                                                            "city": {
                                                                "type": "string",
                                                                # MISSING DESCRIPTION HERE
                                                            },
                                                            "zipcode": {
                                                                "type": "string",
                                                                "description": "ZIP/Postal code",
                                                            },
                                                        },
                                                    },
                                                },
                                            },
                                            "items": {
                                                "type": "array",
                                                "description": "List of ordered items",
                                                "items": {
                                                    "type": "object",
                                                    "properties": {
                                                        "product_id": {
                                                            "type": "integer",
                                                            "description": "Product identifier",
                                                        },
                                                        "quantity": {
                                                            "type": "integer",
                                                            # MISSING DESCRIPTION HERE
                                                        },
                                                        "price": {
                                                            "type": "number",
                                                            "description": "Unit price",
                                                        },
                                                    },
                                                },
                                            },
                                        },
                                    },
                                    "example": {
                                        "customer": {
                                            "name": "John Doe",
                                            "email": "john@example.com",
                                            "address": {
                                                "street": "123 Main St",
                                                "city": "Springfield",
                                                "zipcode": "12345",
                                            },
                                        },
                                        "items": [
                                            {
                                                "product_id": 101,
                                                "quantity": 2,
                                                "price": 29.99,
                                            },
                                        ],
                                    },
                                }
                            },
                        },
                        "responses": {
                            "201": {
                                "description": "Order created successfully",
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "type": "object",
                                            "properties": {
                                                "order_id": {
                                                    "type": "integer",
                                                    "description": "Unique order identifier",
                                                },
                                                "status": {
                                                    "type": "string",
                                                    # MISSING DESCRIPTION HERE
                                                },
                                            },
                                        },
                                        "example": {
                                            "order_id": 12345,
                                            "status": "pending",
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


@app.route("/orders", methods=["POST"])
def create_order():
    """Create a new order."""
    return jsonify({"order_id": 12345, "status": "pending"}), 201


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
