"""Mock server - validates email format in request body, returns 400 for invalid emails."""

import re

from flask import Flask, jsonify, request

app = Flask(__name__)

_EMAIL_RE = re.compile(r"^[^@\s,]+@[^@\s,]+\.[^@\s,]+$")


def _is_valid_email(value):
    return isinstance(value, str) and bool(_EMAIL_RE.match(value))


@app.route("/openapi.json")
def openapi():
    """OpenAPI spec with format: email on the contact endpoint."""
    return jsonify(
        {
            "openapi": "3.0.0",
            "info": {"title": "Contact API", "version": "1.0.0"},
            "paths": {
                "/contact": {
                    "post": {
                        "summary": "Submit a contact form",
                        "requestBody": {
                            "required": True,
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "required": [
                                            "name",
                                            "email",
                                            "message",
                                        ],
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
                                            "message": {
                                                "type": "string",
                                                "description": "Message body",
                                            },
                                        },
                                    },
                                    "example": {
                                        "name": "Alice",
                                        "email": "alice@example.com",
                                        "message": "Hello there!",
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
                                                    "description": "Submission status",
                                                },
                                            },
                                        },
                                        "example": {
                                            "id": 1,
                                            "status": "received",
                                        },
                                    }
                                },
                            },
                            "400": {
                                "description": "Invalid email format",
                                "content": {
                                    "application/json": {
                                        "example": {
                                            "error": "Invalid email format",
                                            "field": "email",
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


@app.route("/contact", methods=["POST"])
def submit_contact():
    """Accept contact form; validate email format strictly."""
    global _next_id
    data = request.get_json(silent=True) or {}

    email = data.get("email", "")
    if not _is_valid_email(email):
        return (
            jsonify({"error": "Invalid email format", "field": "email"}),
            400,
        )

    result = {"id": _next_id, "status": "received"}
    _next_id += 1
    return jsonify(result), 200


@app.route("/reset", methods=["POST"])
def reset():
    """Reset server state."""
    global _next_id
    _next_id = 1
    return jsonify({"status": "reset"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
