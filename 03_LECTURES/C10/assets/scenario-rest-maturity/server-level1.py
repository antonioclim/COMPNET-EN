from __future__ import annotations

from flask import Flask, request, jsonify
from common import initial_users, next_id

app = Flask(__name__)
users = initial_users()

@app.post("/users")
def users_collection_post():
    data = request.get_json(silent=True) or {}
    action = data.get("action")

    if action == "create":
        name = data.get("name")
        if not name:
            return jsonify({"error": "Missing 'name'"}), 400
        user_id = next_id(users)
        users[user_id] = {"id": user_id, "name": name}
        return jsonify(users[user_id]), 201

    return jsonify({"error": "Unknown action for /users", "hint": "action=create"}), 400

@app.post("/users/<int:user_id>")
def user_resource_post(user_id: int):
    data = request.get_json(silent=True) or {}
    action = data.get("action")

    if action == "get":
        user = users.get(user_id)
        if not user:
            return jsonify({"error": "User not found"}), 404
        return jsonify(user), 200

    if action == "update":
        if user_id not in users:
            return jsonify({"error": "User not found"}), 404
        name = data.get("name")
        if not name:
            return jsonify({"error": "Missing 'name'"}), 400
        users[user_id]["name"] = name
        return jsonify(users[user_id]), 200

    if action == "delete":
        if user_id not in users:
            return jsonify({"error": "User not found"}), 404
        del users[user_id]
        return jsonify({"status": "deleted"}), 200

    return jsonify({"error": "Unknown action for /users/<id>", "hint": "action=get|update|delete"}), 400

if __name__ == "__main__":
    app.run(port=5001, debug=True)
