from __future__ import annotations

from flask import Flask, request, jsonify, make_response, url_for
from common import initial_users, next_id

app = Flask(__name__)
users = initial_users()

def user_representation(user_id: int):
    user = users[user_id]
    return {
        "id": user["id"],
        "name": user["name"],
        "links": {
            "self": url_for("get_user", user_id=user_id, _external=False),
            "update": url_for("put_user", user_id=user_id, _external=False),
            "delete": url_for("delete_user", user_id=user_id, _external=False),
            "collection": url_for("list_users", _external=False),
        },
    }

@app.get("/")
def entrypoint():
    return jsonify({
        "name": "Users API (Level 3)",
        "links": {
            "users": url_for("list_users", _external=False),
            "create_user": url_for("create_user", _external=False),
        }
    }), 200

@app.get("/users")
def list_users():
    return jsonify({
        "items": [user_representation(uid) for uid in sorted(users.keys())],
        "links": {
            "self": url_for("list_users", _external=False),
            "create_user": url_for("create_user", _external=False),
        }
    }), 200

@app.post("/users")
def create_user():
    data = request.get_json(silent=True) or {}
    name = data.get("name")
    if not name:
        return jsonify({"error": "Missing 'name'"}), 400

    user_id = next_id(users)
    users[user_id] = {"id": user_id, "name": name}

    resp = make_response(jsonify(user_representation(user_id)), 201)
    resp.headers["Location"] = url_for("get_user", user_id=user_id, _external=False)
    return resp

@app.get("/users/<int:user_id>")
def get_user(user_id: int):
    if user_id not in users:
        return jsonify({"error": "User not found"}), 404
    return jsonify(user_representation(user_id)), 200

@app.put("/users/<int:user_id>")
def put_user(user_id: int):
    if user_id not in users:
        return jsonify({"error": "User not found"}), 404

    data = request.get_json(silent=True) or {}
    name = data.get("name")
    if not name:
        return jsonify({"error": "Missing 'name'"}), 400

    users[user_id]["name"] = name
    return jsonify(user_representation(user_id)), 200

@app.delete("/users/<int:user_id>")
def delete_user(user_id: int):
    if user_id not in users:
        return jsonify({"error": "User not found"}), 404
    del users[user_id]
    return "", 204

if __name__ == "__main__":
    app.run(port=5003, debug=True)
