"""Mock server - POST response missing key that's in example."""

from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route("/openapi.json")
def openapi():
    """OpenAPI spec with complete response example."""
    return jsonify(
        {
            "openapi": "3.0.0",
            "info": {
                "title": "POST Response Missing Key API",
                "version": "1.0.0",
            },
            "paths": {
                "/task": {
                    "post": {
                        "summary": "Create task",
                        "requestBody": {
                            "required": True,
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "properties": {
                                            "title": {
                                                "type": "string",
                                                "description": "Task title",
                                            }
                                        },
                                    },
                                    "example": {"title": "Do laundry"},
                                }
                            },
                        },
                        "responses": {
                            "201": {
                                "description": "Task created",
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "type": "object",
                                            "properties": {
                                                "id": {
                                                    "type": "integer",
                                                    "description": "Task ID",
                                                },
                                                "title": {
                                                    "type": "string",
                                                    "description": "Task title",
                                                },
                                                "status": {
                                                    "type": "string",
                                                    "description": "Task status",
                                                },
                                            },
                                        },
                                        "example": {
                                            "id": 1,
                                            "title": "Do laundry",
                                            "status": "pending",
                                        },
                                    }
                                },
                            }
                        },
                    }
                }
            },
        }
    )


@app.route("/task", methods=["POST"])
def create_task():
    """Create task - MISSING 'status' key in response."""
    data = request.get_json()
    return jsonify({"id": 1, "title": data.get("title")}), 201


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
