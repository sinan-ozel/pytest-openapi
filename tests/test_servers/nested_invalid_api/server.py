"""Mock server with nested schemas and complete descriptions."""

from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route("/openapi.json")
def openapi():
    """Return OpenAPI spec with nested schemas and descriptions."""
    return jsonify(
        {
            "openapi": "3.0.0",
            "info": {"title": "Nested Valid API", "version": "1.0.0"},
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
                                                        "description": "Customer email address",
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
                                                                "description": "City name",
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
                                                            "description": "Quantity ordered",
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
                                            {
                                                "product_id": 202,
                                                "quantity": 1,
                                                "price": 49.99,
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
                                                    "description": "Order status",
                                                },
                                                "total": {
                                                    "type": "number",
                                                    "description": "Total order amount",
                                                },
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
                                                            "description": "Customer email address",
                                                        },
                                                    },
                                                },
                                                "shipping": {
                                                    "type": "object",
                                                    "description": "Shipping details",
                                                    "properties": {
                                                        "estimated_delivery": {
                                                            "type": "string",
                                                            "description": "Estimated delivery date",
                                                        },
                                                        "tracking_number": {
                                                            "type": "string",
                                                            "description": "Shipment tracking number",
                                                        },
                                                    },
                                                },
                                            },
                                        },
                                        "example": {
                                            "order_id": 12345,
                                            "status": "pending",
                                            "total": 109.97,
                                            "customer": {
                                                "name": "John Doe",
                                                "email": "john@example.com",
                                            },
                                            "shipping": {
                                                "estimated_delivery": "2025-12-28",
                                                "tracking_number": "TRK123456789",
                                            },
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
    data = request.get_json()

    # Calculate total
    total = sum(item["quantity"] * item["price"] for item in data.get("items", []))

    return (
        jsonify(
            {
                "order_id": 12345,
                "status": "pending",
                "total": total,
                "customer": {
                    "name": data["customer"]["name"],
                    "email": data["customer"]["email"],
                },
                "shipping": {
                    "estimated_delivery": "2025-12-28",
                    "tracking_number": "TRK123456789",
                },
            }
        ),
        201,
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
