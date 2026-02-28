from __future__ import annotations

from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route("/health")
def health():
    return "ok", 200


@app.route("/users")
def users():
    payload = {
        "users": [
            {"id": 1, "name": "Alice"},
            {"id": 2, "name": "Bob"},
        ],
        "debug": {
            "host": request.host,
            "x_forwarded_for": request.headers.get("X-Forwarded-For"),
            "x_forwarded_proto": request.headers.get("X-Forwarded-Proto"),
        },
    }
    return jsonify(payload)


if __name__ == "__main__":
    # The built-in development server is sufficient for this teaching lab.
    app.run(host="0.0.0.0", port=5000)
