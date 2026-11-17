"""JSON-RPC client for the supplied local teaching server (standard library only)."""
import itertools
import json
import os
from urllib.request import Request, urlopen

URL = os.environ.get("JSONRPC_URL", "http://127.0.0.1:8000/")
REQUEST_IDS = itertools.count(1)


def rpc_call(method, params):
    request_id = next(REQUEST_IDS)
    payload = {"jsonrpc": "2.0", "id": request_id, "method": method, "params": params}
    print("Request payload:", json.dumps(payload, indent=2))
    request = Request(URL, data=json.dumps(payload).encode("utf-8"),
                      headers={"Content-Type": "application/json"}, method="POST")
    with urlopen(request, timeout=5) as response:
        data = json.loads(response.read(65537))
    if not isinstance(data, dict) or data.get("jsonrpc") != "2.0" or data.get("id") != request_id:
        raise ValueError("Invalid JSON-RPC response or mismatched id")
    if ("result" in data) == ("error" in data):
        raise ValueError("Expected exactly one of result and error")
    if "error" in data:
        raise RuntimeError(f"RPC error: {data['error']}")
    return data["result"]


def main():
    print("JSON-RPC Client Demo")
    print("evaluate(2+3) =", rpc_call("evaluate", ["2+3"]))
    # TODO 1: Read a mathematical expression from the keyboard.
    # TODO 2: Call evaluate again; catch and explain transport/RPC errors separately.
    # TODO 3: Print and save the request, matching response id and result or error.


if __name__ == "__main__":
    main()
