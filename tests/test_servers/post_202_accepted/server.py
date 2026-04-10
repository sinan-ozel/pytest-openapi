"""Mock server where POST and GET endpoints respond with 202 Accepted."""

from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route("/openapi.json")
def openapi():
    """Return OpenAPI spec with 202 Accepted responses."""
    return jsonify(
        {
            "openapi": "3.0.0",
            "info": {"title": "202 Accepted API", "version": "1.0.0"},
            "paths": {
                "/jobs": {
                    "post": {
                        "summary": "Submit a background job",
                        "requestBody": {
                            "required": True,
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "required": ["task"],
                                        "properties": {
                                            "task": {
                                                "type": "string",
                                                "description": "Task name to run",
                                            }
                                        },
                                    },
                                    "example": {"task": "generate-report"},
                                }
                            },
                        },
                        "responses": {
                            "202": {
                                "description": "Job accepted and queued",
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "type": "object",
                                            "properties": {
                                                "job_id": {
                                                    "type": "string",
                                                    "description": "Unique job identifier",
                                                },
                                                "status": {
                                                    "type": "string",
                                                    "description": "Initial job status",
                                                },
                                            },
                                        },
                                        "example": {
                                            "job_id": "abc-123",
                                            "status": "queued",
                                        },
                                    }
                                },
                            }
                        },
                    }
                },
                "/jobs/{job_id}": {
                    "get": {
                        "summary": "Check job status",
                        "parameters": [
                            {
                                "name": "job_id",
                                "in": "path",
                                "required": True,
                                "schema": {"type": "string"},
                            }
                        ],
                        "responses": {
                            "202": {
                                "description": "Job is still processing",
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "type": "object",
                                            "properties": {
                                                "job_id": {
                                                    "type": "string",
                                                    "description": "Job identifier",
                                                },
                                                "status": {
                                                    "type": "string",
                                                    "description": "Current job status",
                                                },
                                            },
                                        },
                                        "example": {
                                            "job_id": "abc-123",
                                            "status": "processing",
                                        },
                                    }
                                },
                            }
                        },
                    }
                },
            },
        }
    )


@app.route("/jobs", methods=["POST"])
def submit_job():
    data = request.get_json()
    return jsonify({"job_id": "abc-123", "status": "queued"}), 202


@app.route("/jobs/<job_id>", methods=["GET"])
def get_job(job_id):
    return jsonify({"job_id": job_id, "status": "processing"}), 202


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
