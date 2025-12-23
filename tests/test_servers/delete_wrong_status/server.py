"""Mock server - DELETE returning wrong status code."""

from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/openapi.json")
def openapi():
    """OpenAPI spec expecting 204."""
    return jsonify(
        {
            "openapi": "3.0.0",
            "info": {"title": "DELETE Wrong Status API", "version": "1.0.0"},
            "paths": {
                "/records/{record_id}": {
                    "delete": {
                        "summary": "Delete record",
                        "parameters": [
                            {
                                "name": "record_id",
                                "in": "path",
                                "required": True,
                                "schema": {"type": "integer"},
                            }
                        ],
                        "responses": {
                            "204": {"description": "Record deleted"}
                        },
                    }
                }
            },
        }
    )


@app.route("/records/<int:record_id>", methods=["DELETE"])
def delete_record(record_id):
    """Delete record - RETURNS 500 instead of 204."""
    return jsonify({"error": "Database error"}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
