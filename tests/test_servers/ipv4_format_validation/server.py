"""Mock server - validates IPv4 format in request body, returns descriptive 400."""

import re

from flask import Flask, jsonify, request

app = Flask(__name__)

_IPV4_RE = re.compile(r"^(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})$")


def _is_valid_ipv4(value):
    if not isinstance(value, str):
        return False, "IPv4 address must be a string"
    m = _IPV4_RE.match(value)
    if not m:
        return (
            False,
            "IPv4 address must be four decimal octets separated by dots (e.g. 192.168.1.1)",
        )
    octets = [int(g) for g in m.groups()]
    if any(o > 255 for o in octets):
        bad = [str(o) for o in octets if o > 255]
        return False, f"Each octet must be 0-255; invalid: {', '.join(bad)}"
    return True, None


@app.route("/openapi.json")
def openapi():
    return jsonify(
        {
            "openapi": "3.0.0",
            "info": {"title": "Network API", "version": "1.0.0"},
            "paths": {
                "/allow": {
                    "post": {
                        "summary": "Add an IP address to the allowlist",
                        "requestBody": {
                            "required": True,
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "required": ["ip_address", "label"],
                                        "properties": {
                                            "ip_address": {
                                                "type": "string",
                                                "format": "ipv4",
                                                "description": "IPv4 address to allowlist",
                                            },
                                            "label": {
                                                "type": "string",
                                                "description": "Description of this IP",
                                            },
                                        },
                                    },
                                    "example": {
                                        "ip_address": "192.168.1.1",
                                        "label": "Office network",
                                    },
                                }
                            },
                        },
                        "responses": {
                            "200": {
                                "description": "IP added to allowlist",
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
                                        "example": {
                                            "id": 1,
                                            "status": "allowed",
                                        },
                                    }
                                },
                            },
                            "400": {
                                "description": "Invalid IPv4 address",
                                "content": {
                                    "application/json": {
                                        "example": {
                                            "error": "Invalid IPv4 address",
                                            "field": "ip_address",
                                            "detail": "Each octet must be 0-255",
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


@app.route("/allow", methods=["POST"])
def add_allowlist():
    global _next_id
    data = request.get_json(silent=True) or {}
    ip_address = data.get("ip_address", "")
    valid, reason = _is_valid_ipv4(ip_address)
    if not valid:
        return (
            jsonify(
                {
                    "error": "Invalid IPv4 address",
                    "field": "ip_address",
                    "detail": reason,
                }
            ),
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
