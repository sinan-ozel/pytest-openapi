"""Mock server - validates hostname format in request body, returns descriptive 400."""

import re

from flask import Flask, jsonify, request

app = Flask(__name__)

# Each label: 1-63 chars, alphanumeric or hyphen, must not start/end with hyphen.
# Full hostname: labels joined by '.', total ≤ 253 chars.
_LABEL_RE = re.compile(r"^[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?$")


def _is_valid_hostname(value):
    if not isinstance(value, str) or not value.strip():
        return False, "Hostname must be a non-empty string"
    if len(value) > 253:
        return (
            False,
            f"Hostname exceeds maximum length of 253 characters (got {len(value)})",
        )
    labels = value.rstrip(".").split(".")
    if not labels:
        return False, "Hostname must contain at least one label"
    for label in labels:
        if not label:
            return (
                False,
                "Hostname must not contain consecutive dots or a leading dot",
            )
        if not _LABEL_RE.match(label):
            return (
                False,
                f"Label '{label}' is invalid: each label must be 1-63 alphanumeric characters "
                "or hyphens and must not start or end with a hyphen",
            )
    return True, None


@app.route("/openapi.json")
def openapi():
    return jsonify(
        {
            "openapi": "3.0.0",
            "info": {"title": "Server Config API", "version": "1.0.0"},
            "paths": {
                "/config": {
                    "post": {
                        "summary": "Configure a remote server hostname",
                        "requestBody": {
                            "required": True,
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "required": ["server_hostname", "port"],
                                        "properties": {
                                            "server_hostname": {
                                                "type": "string",
                                                "format": "hostname",
                                                "description": "Fully-qualified hostname of the server",
                                            },
                                            "port": {
                                                "type": "integer",
                                                "description": "Port number",
                                                "minimum": 1,
                                                "maximum": 65535,
                                            },
                                        },
                                    },
                                    "example": {
                                        "server_hostname": "api.example.com",
                                        "port": 443,
                                    },
                                }
                            },
                        },
                        "responses": {
                            "200": {
                                "description": "Server configured",
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "type": "object",
                                            "properties": {
                                                "id": {
                                                    "type": "integer",
                                                    "description": "Config ID",
                                                },
                                                "status": {
                                                    "type": "string",
                                                    "description": "Config status",
                                                },
                                            },
                                        },
                                        "example": {
                                            "id": 1,
                                            "status": "configured",
                                        },
                                    }
                                },
                            },
                            "400": {
                                "description": "Invalid hostname",
                                "content": {
                                    "application/json": {
                                        "example": {
                                            "error": "Invalid hostname",
                                            "field": "server_hostname",
                                            "detail": "Each label must be 1-63 alphanumeric characters or hyphens",
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


@app.route("/config", methods=["POST"])
def configure_server():
    global _next_id
    data = request.get_json(silent=True) or {}
    hostname = data.get("server_hostname", "")
    valid, reason = _is_valid_hostname(hostname)
    if not valid:
        return (
            jsonify(
                {
                    "error": "Invalid hostname",
                    "field": "server_hostname",
                    "detail": reason,
                }
            ),
            400,
        )
    result = {"id": _next_id, "status": "configured"}
    _next_id += 1
    return jsonify(result), 200


@app.route("/reset", methods=["POST"])
def reset():
    global _next_id
    _next_id = 1
    return jsonify({"status": "reset"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
