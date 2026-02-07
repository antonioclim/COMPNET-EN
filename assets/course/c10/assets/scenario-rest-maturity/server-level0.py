from __future__ import annotations

from flask import Flask, request, jsonify
from common import initial_users, next_id

app = Flask(__name__)
users = initial_users()

@app.post("/api")
def rpc_api():
    data = request.get_json(silent=True) or {}
    action = data.get("action")

    if action == "get_user":
        user_id = int(data.get("user_id", 0))
        user = users.get(user_id)
        if not user:
            return jsonify({"error": "User not found"}), 404
        return jsonify(user), 200

    if action == "create_user":
        name = data.get("name")
        if not name:
            return jsonify({"error": "Missing 'name'"}), 400
        user_id = next_id(users)
        users[user_id] = {"id": user_id, "name": name}
        return jsonify(users[user_id]), 201

    if action == "update_user":
        user_id = int(data.get("user_id", 0))
        name = data.get("name")
        if user_id not in users:
            return jsonify({"error": "User not found"}), 404
        if not name:
            return jsonify({"error": "Missing 'name'"}), 400
        users[user_id]["name"] = name
        return jsonify(users[user_id]), 200

    if action == "delete_user":
        user_id = int(data.get("user_id", 0))
        if user_id not in users:
            return jsonify({"error": "User not found"}), 404
        del users[user_id]
        return jsonify({"status": "deleted"}), 200

    return jsonify({"error": "Unknown action", "hint": "use action=get_user|create_user|update_user|delete_user"}), 400

if __name__ == "__main__":
    app.run(port=5000, debug=True)
