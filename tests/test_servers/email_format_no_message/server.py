"""Mock server - validates email but returns 400 with NO descriptive body.

This is a deliberately bad server: it rejects invalid emails with an empty
400 body instead of explaining what went wrong.  The plugin should FAIL
tests against this server because a useful error message is required.
"""

import re

from flask import Flask, jsonify, request

app = Flask(__name__)

_EMAIL_RE = re.compile(r"^[^@\s,]+@[^@\s,]+\.[^@\s,]+$")


@app.route("/openapi.json")
def openapi():
    return jsonify(
        {
            "openapi": "3.0.0",
            "info": {"title": "Contact API (no error messages)", "version": "1.0.0"},
            "paths": {
                "/contact": {
                    "post": {
                        "summary": "Submit contact form",
                        "requestBody": {
                            "required": True,
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "required": ["name", "email"],
                                        "properties": {
                                            "name": {
                                                "type": "string",
                                                "description": "Full name",
                                            },
                                            "email": {
                                                "type": "string",
                                                "format": "email",
                                                "description": "Contact email address",
                                            },
                                        },
                                    },
                                    "example": {
                                        "name": "Alice",
                                        "email": "alice@example.com",
                                    },
                                }
                            },
                        },
                        "responses": {
                            "200": {
                                "description": "Contact form received",
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "type": "object",
                                            "properties": {
                                                "id": {
                                                    "type": "integer",
                                                    "description": "Submission ID",
                                                },
                                                "status": {
                                                    "type": "string",
                                                    "description": "Status",
                                                },
                                            },
                                        },
                                        "example": {"id": 1, "status": "received"},
                                    }
                                },
                            },
                            "400": {
                                "description": "Bad request",
                                "content": {
                                    "application/json": {
                                        "example": {}
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


@app.route("/contact", methods=["POST"])
def submit_contact():
    """Reject invalid emails with 400 but give NO error description."""
    global _next_id
    data = request.get_json(silent=True) or {}
    email = data.get("email", "")
    if not isinstance(email, str) or not _EMAIL_RE.match(email):
        # Deliberately empty body — no error message
        return jsonify({}), 400
    result = {"id": _next_id, "status": "received"}
    _next_id += 1
    return jsonify(result), 200


@app.route("/reset", methods=["POST"])
def reset():
    global _next_id
    _next_id = 1
    return jsonify({"status": "reset"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
