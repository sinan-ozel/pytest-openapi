"""Mock server - validates IPv6 format in request body, returns descriptive 400."""

import socket

from flask import Flask, jsonify, request

app = Flask(__name__)


def _is_valid_ipv6(value):
    if not isinstance(value, str) or not value.strip():
        return False, "IPv6 address must be a non-empty string"
    try:
        socket.inet_pton(socket.AF_INET6, value)
        return True, None
    except (socket.error, OSError):
        return (
            False,
            f"'{value}' is not a valid IPv6 address; "
            "expected format like '2001:db8::1' or '::1'",
        )


@app.route("/openapi.json")
def openapi():
    return jsonify(
        {
            "openapi": "3.0.0",
            "info": {"title": "IPv6 Network API", "version": "1.0.0"},
            "paths": {
                "/allow6": {
                    "post": {
                        "summary": "Add an IPv6 address to the allowlist",
                        "requestBody": {
                            "required": True,
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "required": ["ipv6_address", "label"],
                                        "properties": {
                                            "ipv6_address": {
                                                "type": "string",
                                                "format": "ipv6",
                                                "description": "IPv6 address to allowlist",
                                            },
                                            "label": {
                                                "type": "string",
                                                "description": "Description of this address",
                                            },
                                        },
                                    },
                                    "example": {
                                        "ipv6_address": "2001:0db8:85a3:0000:0000:8a2e:0370:7334",
                                        "label": "Remote office",
                                    },
                                }
                            },
                        },
                        "responses": {
                            "200": {
                                "description": "IPv6 address added to allowlist",
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "type": "object",
                                            "properties": {
                                                "id": {
                                                    "type": "integer",
                                                    "description": "Rule ID",
                                                },
                                                "status": {
                                                    "type": "string",
                                                    "description": "Rule status",
                                                },
                                            },
                                        },
                                        "example": {"id": 1, "status": "allowed"},
                                    }
                                },
                            },
                            "400": {
                                "description": "Invalid IPv6 address",
                                "content": {
                                    "application/json": {
                                        "example": {
                                            "error": "Invalid IPv6 address",
                                            "field": "ipv6_address",
                                            "detail": "expected format like '2001:db8::1' or '::1'",
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


@app.route("/allow6", methods=["POST"])
def add_allowlist_ipv6():
    global _next_id
    data = request.get_json(silent=True) or {}
    ipv6_address = data.get("ipv6_address", "")
    valid, reason = _is_valid_ipv6(ipv6_address)
    if not valid:
        return (
            jsonify({"error": "Invalid IPv6 address", "field": "ipv6_address", "detail": reason}),
            400,
        )
    result = {"id": _next_id, "status": "allowed"}
    _next_id += 1
    return jsonify(result), 200


@app.route("/reset", methods=["POST"])
def reset():
    global _next_id
    _next_id = 1
    return jsonify({"status": "reset"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
