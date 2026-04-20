"""Mock server - validates URI format in request body, returns descriptive 400."""

from urllib.parse import urlparse

from flask import Flask, jsonify, request

app = Flask(__name__)

_VALID_SCHEMES = {"http", "https", "ftp", "ftps"}


def _is_valid_uri(value):
    if not isinstance(value, str) or not value.strip():
        return False, "URI must be a non-empty string"
    try:
        parsed = urlparse(value)
    except Exception:
        return False, "URI could not be parsed"
    if not parsed.scheme:
        return False, "URI must include a scheme (e.g. https://)"
    if parsed.scheme not in _VALID_SCHEMES:
        return False, f"URI scheme '{parsed.scheme}' is not supported; use one of {sorted(_VALID_SCHEMES)}"
    if not parsed.netloc:
        return False, "URI must include a host"
    return True, None


@app.route("/openapi.json")
def openapi():
    return jsonify(
        {
            "openapi": "3.0.0",
            "info": {"title": "Webhook API", "version": "1.0.0"},
            "paths": {
                "/webhook": {
                    "post": {
                        "summary": "Register a webhook callback",
                        "requestBody": {
                            "required": True,
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "required": ["callback_url", "event"],
                                        "properties": {
                                            "callback_url": {
                                                "type": "string",
                                                "format": "uri",
                                                "description": "Callback URL for webhook delivery",
                                            },
                                            "event": {
                                                "type": "string",
                                                "description": "Event type to subscribe to",
                                            },
                                        },
                                    },
                                    "example": {
                                        "callback_url": "https://example.com/hook",
                                        "event": "order.created",
                                    },
                                }
                            },
                        },
                        "responses": {
                            "200": {
                                "description": "Webhook registered",
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "type": "object",
                                            "properties": {
                                                "id": {
                                                    "type": "integer",
                                                    "description": "Webhook ID",
                                                },
                                                "status": {
                                                    "type": "string",
                                                    "description": "Registration status",
                                                },
                                            },
                                        },
                                        "example": {"id": 1, "status": "registered"},
                                    }
                                },
                            },
                            "400": {
                                "description": "Invalid URI format",
                                "content": {
                                    "application/json": {
                                        "example": {
                                            "error": "Invalid URI format",
                                            "field": "callback_url",
                                            "detail": "URI must include a scheme (e.g. https://)",
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


_next_id = 1


@app.route("/webhook", methods=["POST"])
def register_webhook():
    global _next_id
    data = request.get_json(silent=True) or {}
    callback_url = data.get("callback_url", "")
    valid, reason = _is_valid_uri(callback_url)
    if not valid:
        return (
            jsonify({"error": "Invalid URI format", "field": "callback_url", "detail": reason}),
            400,
        )
    result = {"id": _next_id, "status": "registered"}
    _next_id += 1
    return jsonify(result), 200


@app.route("/reset", methods=["POST"])
def reset():
    global _next_id
    _next_id = 1
    return jsonify({"status": "reset"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
