from __future__ import annotations

from typing import Dict, Any

def initial_users() -> Dict[int, Dict[str, Any]]:
    return {
        1: {"id": 1, "name": "Alice"},
        2: {"id": 2, "name": "Bob"},
    }

def next_id(users: Dict[int, Dict[str, Any]]) -> int:
    if not users:
        return 1
    return max(users.keys()) + 1
