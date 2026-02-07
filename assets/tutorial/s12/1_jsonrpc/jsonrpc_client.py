
import requests
import json

URL = "https://api.mathjs.org/v4/"

def rpc_call(method, params):
    """
    Construiește un request JSON-RPC standard și îl trimite către server.
    """
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": method,
        "params": params
    }

    response = requests.post(URL, json=payload)

    # Afișăm pentru debugging
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

    # Apel de test
    result = rpc_call("evaluate", ["2+3"])
    print("evaluate(2+3) =", result)

    # TODO 1: Citiți o expresie matematică de la tastatură
    # expr = ...

    # TODO 2: Apelați din nou metoda evaluate
    # result = ...

    # TODO 3: Afișați rezultatul
    # print("Rezultatul este:", result)


if __name__ == "__main__":
    main()
