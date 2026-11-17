from __future__ import annotations

import json
from threading import RLock
from typing import Dict, List, Any, Tuple

from flask import Flask, send_from_directory
from flask_sock import Sock

app = Flask(__name__)
sock = Sock(app)

# state
clients: List[Tuple[Any, Dict[str, Any]]] = []
room_counters: Dict[str, int] = {}
state_lock = RLock()

@app.get("/")
def index():
    return send_from_directory(".", "index.html")

def ws_send(ws, obj: Dict[str, Any]):
    try:
        ws.send(json.dumps(obj))
        return True
    except Exception:  # WebSocket backends expose different connection-closed exception types.
        return False

@sock.route("/ws")
def ws_endpoint(ws):
    state = {
        "joined": False,
        "room": None,
        "name": None,
    }
    with state_lock:
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

            if not isinstance(msg, dict):
                ws_send(ws, {"type": "error", "message": "message must be a JSON object"})
                continue
            mtype = msg.get("type")

            if mtype == "join":
                room = msg.get("room")
                name = msg.get("name")
                if not isinstance(room, str) or not room.strip() or not isinstance(name, str) or not name.strip():
                    ws_send(ws, {"type": "error", "message": "join requires room and name"})
                    continue
                with state_lock:
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
                if not isinstance(text, str) or not text.strip():
                    ws_send(ws, {"type": "error", "message": "empty text"})
                    continue

                with state_lock:
                    room_counters[room] += 1
                    msg_id = room_counters[room]
                    recipients = [(peer, dict(peer_state)) for peer, peer_state in clients]

                deliver = {
                    "type": "deliver",
                    "room": room,
                    "from": state["name"],
                    "text": text,
                    "id": msg_id,
                }

                # broadcast to same room
                for (other_ws, other_state) in recipients:
                    if other_state.get("joined") and other_state.get("room") == room:
                        if not ws_send(other_ws, deliver):
                            with state_lock:
                                clients[:] = [(c, st) for c, st in clients if c is not other_ws]

                # ack sender
                ws_send(ws, {"type": "ack", "id": msg_id})
                continue

            ws_send(ws, {"type": "error", "message": "unknown type"})
    finally:
        with state_lock:
            clients[:] = [(c, st) for c, st in clients if c is not ws]

if __name__ == "__main__":
    app.run(port=9000, debug=True)
