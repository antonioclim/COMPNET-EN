from __future__ import annotations

from flask import Flask, jsonify, request

app = Flask(__name__)

@app.get("/users")
def users():
    return jsonify({
        "users": [
            {"id": 1, "name": "Alice"},
            {"id": 2, "name": "Bob"},
        ],
        "debug": {
            "host": request.headers.get("Host"),
            "x_forwarded_for": request.headers.get("X-Forwarded-For"),
            "x_forwarded_proto": request.headers.get("X-Forwarded-Proto"),
        }
    }), 200

@app.get("/health")
def health():
    return jsonify({"ok": True}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
