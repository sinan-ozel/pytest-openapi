"""Mock server - GET endpoint with missing key in actual response."""

from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/openapi.json")
def openapi():
    """OpenAPI spec with complete example."""
    return jsonify(
        {
            "openapi": "3.0.0",
            "info": {"title": "GET Missing Key API", "version": "1.0.0"},
            "paths": {
                "/product": {
                    "get": {
                        "summary": "Get product",
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
                                                    "description": "Product ID",
                                                },
                                                "name": {
                                                    "type": "string",
                                                    "description": "Product name",
                                                },
                                                "price": {
                                                    "type": "number",
                                                    "description": "Product price",
                                                },
                                            },
                                        },
                                        "example": {
                                            "id": 1,
                                            "name": "Widget",
                                            "price": 9.99,
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


@app.route("/product")
def get_product():
    """Get product - MISSING 'price' key."""
    return jsonify({"id": 1, "name": "Widget"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
