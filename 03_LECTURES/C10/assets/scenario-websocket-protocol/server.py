from __future__ import annotations

import json
from typing import Dict, List, Any, Tuple

from flask import Flask, send_from_directory
from flask_sock import Sock

app = Flask(__name__)
sock = Sock(app)

# state
clients: List[Tuple[Any, Dict[str, Any]]] = []
room_counters: Dict[str, int] = {}

@app.get("/")
def index():
    return send_from_directory(".", "index.html")

def ws_send(ws, obj: Dict[str, Any]):
    ws.send(json.dumps(obj))

@sock.route("/ws")
def ws_endpoint(ws):
    state = {
        "joined": False,
        "room": None,
        "name": None,
    }
    clients.append((ws, state))

    try:
        while True:
            raw = ws.receive()
            if raw is None:
                break

            try:
                msg = json.loads(raw)
            except Exception:
                ws_send(ws, {"type": "error", "message": "invalid JSON"})
                continue

            mtype = msg.get("type")

            if mtype == "join":
                room = msg.get("room")
                name = msg.get("name")
                if not room or not name:
                    ws_send(ws, {"type": "error", "message": "join requires room and name"})
                    continue
                state["joined"] = True
                state["room"] = room
                state["name"] = name
                room_counters.setdefault(room, 0)
                ws_send(ws, {"type": "joined", "room": room, "you": name})
                continue

            if mtype == "msg":
                if not state["joined"]:
                    ws_send(ws, {"type": "error", "message": "must join first"})
                    continue

                room = msg.get("room")
                text = msg.get("text")
                if room != state["room"]:
                    ws_send(ws, {"type": "error", "message": "wrong room"})
                    continue
                if not text:
                    ws_send(ws, {"type": "error", "message": "empty text"})
                    continue

                room_counters[room] += 1
                msg_id = room_counters[room]

                deliver = {
                    "type": "deliver",
                    "room": room,
                    "from": state["name"],
                    "text": text,
                    "id": msg_id,
                }

                # broadcast to same room
                for (other_ws, other_state) in clients:
                    if other_state.get("joined") and other_state.get("room") == room:
                        ws_send(other_ws, deliver)

                # ack sender
                ws_send(ws, {"type": "ack", "id": msg_id})
                continue

            ws_send(ws, {"type": "error", "message": "unknown type"})
    finally:
        # remove client
        for i, (cws, _) in enumerate(list(clients)):
            if cws == ws:
                clients.pop(i)
                break

if __name__ == "__main__":
    app.run(port=9000, debug=True)
