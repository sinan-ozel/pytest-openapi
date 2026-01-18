"""Mock server - POST endpoint returning 501 without it being documented."""

from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route("/openapi.json")
def openapi():
    """OpenAPI spec expecting 200 response, but 501 is NOT documented."""
    return jsonify(
        {
            "openapi": "3.0.0",
            "info": {"title": "POST 501 Undocumented API", "version": "1.0.0"},
            "paths": {
                "/generate": {
                    "post": {
                        "summary": "Generate completion",
                        "requestBody": {
                            "required": True,
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "properties": {
                                            "prompt": {
                                                "type": "string",
                                                "description": "Text prompt",
                                            },
                                            "stream": {
                                                "type": "boolean",
                                                "default": False,
                                                "description": "Whether to stream",
                                            },
                                        },
                                        "required": ["prompt"],
                                    },
                                    "example": {
                                        "prompt": "Hello",
                                        "stream": False,
                                    },
                                }
                            },
                        },
                        "responses": {
                            "200": {
                                "description": "Completion generated",
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "type": "object",
                                            "properties": {
                                                "response": {
                                                    "type": "string",
                                                    "description": "Generated text",
                                                }
                                            },
                                        },
                                        "example": {"response": "Hello there!"},
                                    }
                                },
                            }
                            # Note: 501 is NOT documented here
                        },
                    }
                }
            },
        }
    )


@app.route("/generate", methods=["POST"])
def generate():
    """Return 501 for streaming requests."""
    data = request.get_json()

    if data.get("stream"):
        return jsonify({"detail": "Streaming not implemented"}), 501

    return jsonify({"response": "Hello there!"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
