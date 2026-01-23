"""Mock server - GET endpoint that returns 404 with documented response."""

from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/openapi.json")
def openapi():
    """OpenAPI spec with 404 as a documented response."""
    return jsonify(
        {
            "openapi": "3.0.0",
            "info": {"title": "GET Returns 404 API", "version": "1.0.0"},
            "paths": {
                "/private/v1/providers/{provider}/max-context-window": {
                    "get": {
                        "summary": "Get max context window for provider",
                        "parameters": [
                            {
                                "name": "provider",
                                "in": "path",
                                "required": True,
                                "schema": {"type": "string"},
                                "description": "Provider name",
                            }
                        ],
                        "responses": {
                            "200": {
                                "description": "Successful response",
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "type": "object",
                                            "properties": {
                                                "provider": {
                                                    "type": "string",
                                                    "description": "Provider name",
                                                },
                                                "max_context_window": {
                                                    "type": "integer",
                                                    "description": "Max context window size",
                                                },
                                            },
                                        },
                                        "example": {
                                            "provider": "pixtral",
                                            "max_context_window": 128000,
                                        },
                                    }
                                },
                            },
                            "404": {
                                "description": "Provider not found",
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "type": "object",
                                            "properties": {
                                                "detail": {
                                                    "type": "string",
                                                    "description": "Error message",
                                                }
                                            },
                                        },
                                        "example": {
                                            "detail": "Provider '{provider}' not found"
                                        },
                                    }
                                },
                            },
                        },
                    }
                }
            },
        }
    )


@app.route("/private/v1/providers/<provider>/max-context-window")
def get_max_context_window(provider):
    """Get max context window - returns 404 for placeholder value."""
    # Return 404 for the placeholder provider value from the example
    return jsonify({"detail": f"Provider '{{provider}}' not found"}), 404


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
