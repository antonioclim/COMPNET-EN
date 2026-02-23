import requests
import json

URL = "https://api.mathjs.org/v4/"

def rpc_call(method, params):
    """
    Build a standard JSON-RPC request and send it to the server.
    """
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": method,
        "params": params
    }

    response = requests.post(URL, json=payload)

    # Print for debugging
    print("Request payload:", json.dumps(payload, indent=2))

    if response.status_code != 200:
        print("HTTP error:", response.status_code)
        return None

    try:
        data = response.json()
        return data.get("result", data.get("error"))
    except ValueError:
        print("Could not decode JSON response.")
        return None


def main():
    print("JSON-RPC Client Demo")

    # Test call
    result = rpc_call("evaluate", ["2+3"])
    print("evaluate(2+3) =", result)

    # TODO 1: Read a mathematical expression from the keyboard
    # expr = ...

    # TODO 2: Call the evaluate method again
    # result = ...

    # TODO 3: Print the result
    # print("Result:", result)


if __name__ == "__main__":
    main()
