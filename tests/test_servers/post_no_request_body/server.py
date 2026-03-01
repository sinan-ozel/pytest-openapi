"""Mock server with a POST endpoint that has no request body (path param only)."""

from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/openapi.json")
def openapi():
    """Return OpenAPI spec with a POST endpoint that has no request body."""
    return jsonify(
        {
            "openapi": "3.0.0",
            "info": {"title": "Cancel Job API", "version": "1.0.0"},
            "paths": {
                "/cancel/{job_id}": {
                    "post": {
                        "summary": "Cancel a job by ID",
                        "parameters": [
                            {
                                "name": "job_id",
                                "in": "path",
                                "required": True,
                                "schema": {"type": "integer"},
                            }
                        ],
                        "responses": {
                            "200": {
                                "description": "Job cancelled successfully",
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "type": "object",
                                            "properties": {
                                                "message": {
                                                    "type": "string",
                                                    "description": "Status message",
                                                },
                                                "job_id": {
                                                    "type": "integer",
                                                    "description": "Cancelled job ID",
                                                },
                                            },
                                        },
                                        "example": {
                                            "message": "Job cancelled",
                                            "job_id": 1,
                                        },
                                    }
                                },
                            },
                            "404": {
                                "description": "Job not found",
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "type": "object",
                                            "properties": {
                                                "error": {
                                                    "type": "string",
                                                    "description": "Error message",
                                                }
                                            },
                                        },
                                        "example": {"error": "Job not found"},
                                    }
                                },
                            },
                        },
                    }
                }
            },
        }
    )


@app.route("/cancel/<int:job_id>", methods=["POST"])
def cancel_job(job_id):
    """Cancel a job. No request body needed."""
    return jsonify({"message": "Job cancelled", "job_id": job_id})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
