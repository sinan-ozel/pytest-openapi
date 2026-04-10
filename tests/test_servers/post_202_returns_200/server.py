"""Mock server that documents 202 Accepted but incorrectly returns 200 OK."""

from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route("/openapi.json")
def openapi():
    return jsonify(
        {
            "openapi": "3.0.0",
            "info": {"title": "202 Mismatch API", "version": "1.0.0"},
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
                                        "example": {
                                            "job_id": "abc-123",
                                            "status": "queued",
                                        }
                                    }
                                },
                            }
                        },
                    }
                }
            },
        }
    )


@app.route("/jobs", methods=["POST"])
def submit_job():
    # Bug: spec says 202 but server returns 200
    return jsonify({"job_id": "abc-123", "status": "queued"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
