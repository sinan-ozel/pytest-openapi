"""Mock server - Email API with POST endpoint to save an email."""

from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route("/openapi.json")
def openapi():
    """OpenAPI spec for the Email API."""
    return jsonify(
        {
            "openapi": "3.0.0",
            "info": {"title": "Email API", "version": "1.0.0"},
            "paths": {
                "/email": {
                    "post": {
                        "summary": "Save an email",
                        "requestBody": {
                            "required": True,
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "required": ["to", "from", "subject", "body"],
                                        "properties": {
                                            "to": {
                                                "type": "string",
                                                "description": "Recipient email address",
                                            },
                                            "from": {
                                                "type": "string",
                                                "description": "Sender email address",
                                            },
                                            "subject": {
                                                "type": "string",
                                                "description": "Email subject",
                                            },
                                            "body": {
                                                "type": "string",
                                                "description": "Email body",
                                            },
                                        },
                                    },
                                    "example": {
                                        "to": "bob@example.com",
                                        "from": "alice@example.com",
                                        "subject": "Hello",
                                        "body": "Hi Bob, how are you?",
                                    },
                                }
                            },
                        },
                        "responses": {
                            "201": {
                                "description": "Email saved",
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "type": "object",
                                            "properties": {
                                                "id": {
                                                    "type": "integer",
                                                    "description": "Email ID",
                                                },
                                                "to": {
                                                    "type": "string",
                                                    "description": "Recipient email address",
                                                },
                                                "from": {
                                                    "type": "string",
                                                    "description": "Sender email address",
                                                },
                                                "subject": {
                                                    "type": "string",
                                                    "description": "Email subject",
                                                },
                                                "body": {
                                                    "type": "string",
                                                    "description": "Email body",
                                                },
                                            },
                                        },
                                        "example": {
                                            "id": 1,
                                            "to": "bob@example.com",
                                            "from": "alice@example.com",
                                            "subject": "Hello",
                                            "body": "Hi Bob, how are you?",
                                        },
                                    }
                                }
                            }
                        }
                    }
                },
                "/email_bad": {
                    "post": {
                        "summary": "Save an email (bad response)",
                        "requestBody": {
                            "required": True,
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "required": ["to", "from", "subject", "body"],
                                        "properties": {
                                            "to": {"type": "string", "description": "Recipient email address"},
                                            "from": {"type": "string", "description": "Sender email address"},
                                            "subject": {"type": "string", "description": "Email subject"},
                                            "body": {"type": "string", "description": "Email body"},
                                        },
                                    },
                                    "example": {
                                        "to": "bob@example.com",
                                        "from": "alice@example.com",
                                        "subject": "Hello",
                                        "body": "Hi Bob, how are you?",
                                    },
                                }
                            },
                        },
                        "responses": {
                            "201": {
                                "description": "Email saved (bad subject type)",
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "type": "object",
                                            "properties": {
                                                "id": {"type": "integer", "description": "Email ID"},
                                                "to": {"type": "string", "description": "Recipient email address"},
                                                "from": {"type": "string", "description": "Sender email address"},
                                                "subject": {"type": "string", "description": "Email subject"},
                                                "body": {"type": "string", "description": "Email body"},
                                            }
                                        },
                                        "example": {
                                            "id": 1,
                                            "to": "bob@example.com",
                                            "from": "alice@example.com",
                                            "subject": "Hello",
                                            "body": "Hi Bob, how are you?",
                                        },
                                    }
                                },
                            }
                        }
                    }
                }
            },
        }
    )


emails_db = {}
next_id = 1


@app.route("/email", methods=["POST"])
def save_email():
    """Save an email and return created resource."""
    global next_id
    data = request.get_json()

    required = ("to", "from", "subject", "body")
    if not data or any(k not in data for k in required):
        return jsonify({"error": "Missing required field"}), 422

    email = {
        "id": next_id,
        "to": data["to"],
        "from": data["from"],
        "subject": data["subject"],
        "body": data["body"],
    }
    emails_db[next_id] = email
    next_id += 1

    return jsonify(email), 201


@app.route("/email_bad", methods=["POST"])
def save_email_bad():
    """Save an email but return wrong type for `subject` (int)."""
    global next_id
    data = request.get_json()

    required = ("to", "from", "subject", "body")
    if not data or any(k not in data for k in required):
        return jsonify({"error": "Missing required field"}), 422

    # Intentionally return subject as integer to simulate type mismatch
    email = {
        "id": next_id,
        "to": data["to"],
        "from": data["from"],
        "subject": 12345,
        "body": data["body"],
    }
    emails_db[next_id] = email
    next_id += 1

    return jsonify(email), 201


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
