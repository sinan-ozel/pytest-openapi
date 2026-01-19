"""Mock server - Response structure matches but values differ from example."""

from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route("/openapi.json")
def openapi():
    """OpenAPI spec with example containing placeholder values."""
    return jsonify(
        {
            "openapi": "3.0.0",
            "info": {
                "title": "Example Value Mismatch API",
                "version": "1.0.0",
            },
            "paths": {
                "/generate": {
                    "post": {
                        "summary": "Generate response",
                        "requestBody": {
                            "required": True,
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "properties": {
                                            "prompt": {
                                                "type": "string",
                                                "description": "Input prompt",
                                            },
                                            "temperature": {
                                                "type": "number",
                                                "description": "Temperature",
                                            },
                                        },
                                    },
                                    "example": {
                                        "prompt": "What is the capital of France?",
                                        "temperature": 0.7,
                                    },
                                }
                            },
                        },
                        "responses": {
                            "200": {
                                "description": "Successful response",
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "type": "object",
                                            "required": [
                                                "response",
                                                "done",
                                                "context",
                                                "eval_count",
                                            ],
                                            "properties": {
                                                "response": {
                                                    "type": "string",
                                                    "description": "Generated response",
                                                },
                                                "done": {
                                                    "type": "boolean",
                                                    "description": "Completion flag",
                                                },
                                                "context": {
                                                    "type": "array",
                                                    "items": {
                                                        "type": "integer"
                                                    },
                                                    "description": "Context tokens",
                                                },
                                                "total_duration": {
                                                    "type": "integer",
                                                    "description": "Total duration in nanoseconds",
                                                },
                                                "eval_count": {
                                                    "type": "integer",
                                                    "description": "Number of evaluations",
                                                },
                                            },
                                        },
                                        "example": {
                                            "response": "The capital of France is Paris.",
                                            "done": True,
                                            "context": [1, 2, 3],
                                            "total_duration": 1000000000,
                                            "eval_count": 10,
                                        },
                                    }
                                },
                            }
                        },
                    }
                },
                "/status": {
                    "get": {
                        "summary": "Get status",
                        "responses": {
                            "200": {
                                "description": "Status response",
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "type": "object",
                                            "required": ["status", "metrics"],
                                            "properties": {
                                                "status": {
                                                    "type": "string",
                                                    "description": "Status message",
                                                },
                                                "metrics": {
                                                    "type": "array",
                                                    "items": {"type": "number"},
                                                    "description": "Metrics data",
                                                },
                                            },
                                        },
                                        "example": {
                                            "status": "healthy",
                                            "metrics": [1.0, 2.5, 3.7],
                                        },
                                    }
                                },
                            }
                        },
                    }
                },
            },
            "/config/{config_id}": {
                "put": {
                    "summary": "Update configuration",
                    "parameters": [
                        {
                            "name": "config_id",
                            "in": "path",
                            "required": True,
                            "schema": {"type": "integer"},
                        }
                    ],
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "name": {
                                            "type": "string",
                                            "description": "Config name",
                                        },
                                        "value": {
                                            "type": "number",
                                            "description": "Config value",
                                        },
                                    },
                                },
                                "example": {
                                    "name": "timeout",
                                    "value": 30.0,
                                },
                            }
                        },
                    },
                    "responses": {
                        "200": {
                            "description": "Configuration updated",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "required": [
                                            "config_id",
                                            "name",
                                            "value",
                                            "history",
                                        ],
                                        "properties": {
                                            "config_id": {
                                                "type": "integer",
                                                "description": "Configuration ID",
                                            },
                                            "name": {
                                                "type": "string",
                                                "description": "Config name",
                                            },
                                            "value": {
                                                "type": "number",
                                                "description": "Config value",
                                            },
                                            "history": {
                                                "type": "array",
                                                "items": {"type": "number"},
                                                "description": "Value history",
                                            },
                                        },
                                    },
                                    "example": {
                                        "config_id": 1,
                                        "name": "timeout",
                                        "value": 30.0,
                                        "history": [20.0, 25.0, 30.0],
                                    },
                                }
                            },
                        }
                    },
                }
            },
        }
    )


@app.route("/generate", methods=["POST"])
def generate():
    """Return response with different values than example (but same structure)."""
    # Actual implementation returns empty context and zero durations
    return jsonify(
        {
            "response": "The capital of France is Paris.",
            "done": True,
            "context": [],  # Empty array instead of [1, 2, 3]
            "total_duration": 0,  # Zero instead of 1000000000
            "eval_count": 5,  # Different value than example
        }
    )


@app.route("/config/<int:config_id>", methods=["PUT"])
def update_config(config_id):
    """Return response with different array values than example."""
    return jsonify(
        {
            "config_id": config_id,
            "name": "timeout",
            "value": 35.0,  # Different value than example (30.0)
            "history": [35.0],  # Only 1 element instead of 3
        }
    )


@app.route("/status")
def status():
    """Return status with different array length than example."""
    return jsonify(
        {
            "status": "healthy",
            "metrics": [0.5],  # Only 1 element instead of 3
        }
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
