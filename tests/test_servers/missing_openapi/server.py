"""Mock server that is missing the /openapi.json endpoint."""

from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/health")
def health():
    """Health check endpoint."""
    return jsonify({"status": "ok"})


@app.route("/users", methods=["GET"])
def get_users():
    """Example endpoint that exists but has no OpenAPI documentation."""
    return jsonify([{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}])


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
