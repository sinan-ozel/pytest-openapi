"""Mock server - validates URI format including port-number range.

Port rules:
  - No port in URL           → valid (uses the scheme default)
  - Port 1–65535             → valid
  - Port 0                   → invalid (reserved, not usable for HTTP)
  - Port > 65535             → invalid (exceeds 16-bit range)
"""

from urllib.parse import urlparse

from flask import Flask, jsonify, request

app = Flask(__name__)

_VALID_SCHEMES = {"http", "https"}


def _validate_url_with_port(value):
    """Return (is_valid, error_detail)."""
    if not isinstance(value, str) or not value.strip():
        return False, "URL must be a non-empty string"
    try:
        parsed = urlparse(value)
    except Exception:
        return False, "URL could not be parsed"
    if not parsed.scheme or parsed.scheme not in _VALID_SCHEMES:
        return (
            False,
            f"URL scheme must be http or https, got '{parsed.scheme or '(none)'}'",
        )
    if not parsed.hostname:
        return False, "URL must include a hostname"
    if parsed.port is not None:
        if parsed.port == 0:
            return False, "Port 0 is reserved and not valid for HTTP URLs"
        if parsed.port > 65535:
            return (
                False,
                f"Port {parsed.port} exceeds the maximum valid port number (65535)",
            )
    return True, None


@app.route("/openapi.json")
def openapi():
    return jsonify(
        {
            "openapi": "3.0.0",
            "info": {"title": "Webhook Port API", "version": "1.0.0"},
            "paths": {
                "/webhook": {
                    "post": {
                        "summary": "Register a webhook; URL port must be in range 1-65535",
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
                                                "description": (
                                                    "Callback URL; port (if given) must be 1-65535. "
                                                    "Port 0 and ports above 65535 are rejected."
                                                ),
                                            },
                                            "event": {
                                                "type": "string",
                                                "description": "Event type",
                                            },
                                        },
                                    },
                                    "example": {
                                        "callback_url": "https://example.com:8080/hook",
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
                                        "example": {
                                            "id": 1,
                                            "status": "registered",
                                        },
                                    }
                                },
                            },
                            "400": {
                                "description": "Invalid URL or port number",
                                "content": {
                                    "application/json": {
                                        "example": {
                                            "error": "Invalid URL or port number",
                                            "field": "callback_url",
                                            "detail": "Port 0 is reserved and not valid for HTTP URLs",
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
    valid, reason = _validate_url_with_port(callback_url)
    if not valid:
        return (
            jsonify(
                {
                    "error": "Invalid URL or port number",
                    "field": "callback_url",
                    "detail": reason,
                }
            ),
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
