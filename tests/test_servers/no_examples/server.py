"""Mock server with OpenAPI spec but without examples."""

from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/openapi.json")
def openapi():
    """Return OpenAPI spec WITHOUT examples (intentionally incomplete)."""
    return jsonify({
        "openapi": "3.0.0",
        "info": {
            "title": "No Examples API",
            "version": "1.0.0"
        },
        "paths": {
            "/products": {
                "get": {
                    "summary": "Get all products",
                    "responses": {
                        "200": {
                            "description": "Successful response",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "array",
                                        "items": {
                                            "type": "object",
                                            "required": ["id", "name", "price"],
                                            "properties": {
                                                "id": {"type": "integer"},
                                                "name": {"type": "string"},
                                                "price": {"type": "number"}
                                            }
                                        }
                                    }
                                    # Note: No "example" or "examples" field here
                                }
                            }
                        }
                    }
                }
            }
        }
    })


@app.route("/products")
def get_products():
    """Get all products endpoint."""
    return jsonify([
        {"id": 1, "name": "Widget", "price": 9.99},
        {"id": 2, "name": "Gadget", "price": 19.99}
    ])


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
