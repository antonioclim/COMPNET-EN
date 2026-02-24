from __future__ import annotations

from flask import Flask, request, jsonify, make_response
from common import initial_users, next_id

app = Flask(__name__)
users = initial_users()

@app.get("/users")
def list_users():
    return jsonify(list(users.values())), 200

@app.post("/users")
def create_user():
    data = request.get_json(silent=True) or {}
    name = data.get("name")
    if not name:
        return jsonify({"error": "Missing 'name'"}), 400

    user_id = next_id(users)
    users[user_id] = {"id": user_id, "name": name}

    resp = make_response(jsonify(users[user_id]), 201)
    resp.headers["Location"] = f"/users/{user_id}"
    return resp

@app.get("/users/<int:user_id>")
def get_user(user_id: int):
    user = users.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify(user), 200

@app.put("/users/<int:user_id>")
def put_user(user_id: int):
    if user_id not in users:
        return jsonify({"error": "User not found"}), 404

    data = request.get_json(silent=True) or {}
    name = data.get("name")
    if not name:
        return jsonify({"error": "Missing 'name'"}), 400

    users[user_id]["name"] = name
    return jsonify(users[user_id]), 200

@app.delete("/users/<int:user_id>")
def delete_user(user_id: int):
    if user_id not in users:
        return jsonify({"error": "User not found"}), 404
    del users[user_id]
    return "", 204

if __name__ == "__main__":
    app.run(port=5002, debug=True)
