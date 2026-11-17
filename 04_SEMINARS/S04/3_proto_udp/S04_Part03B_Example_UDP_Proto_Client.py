import socket
import sys

from S04_Part03_Script_Transfer_Units import (
    RequestMessage,
    RequestMessageType,
    ResponseMessage,
    ResponseMessageType,
)
from S04_Part03_Script_Serialization import serialize, deserialize


def main():
    """
    Interactive UDP client for the mini-protocol.

    Commands (at the "storage>" prompt):

      connect
      send <text...>
      list
      disconnect
      exit   (only closes the client; does not send anything special)
    """

    if len(sys.argv) < 3:
        print(f"Usage: {sys.argv[0]} <HOST> <PORT>")
        sys.exit(1)

    HOST, PORT = sys.argv[1:3]
    PORT = int(PORT)

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client_socket:
        client_socket.settimeout(5)
        print(f"[INFO] UDP client ready, sending to {HOST}:{PORT}")

        while True:
            data = input("storage> ").strip()

            if not data:
                continue

            if data == "exit":
                print("[INFO] Exiting client.")
                break

            # Split the command into at most 2 parts: command + rest.
            items = data.split(" ", 1)
            command = items[0]

            # Build the RequestMessage based on the command.
            if command == "connect":
                request = RequestMessage(RequestMessageType.CONNECT)

            elif command == "list":
                request = RequestMessage(RequestMessageType.LIST)

            elif command == "send":
                if len(items) < 2:
                    print("[WARN] send requires a payload")
                    continue
                payload = items[1]
                request = RequestMessage(RequestMessageType.SEND, payload)

            elif command == "disconnect":
                request = RequestMessage(RequestMessageType.DISCONNECT)

            else:
                print("[WARN] unknown command")
                continue

            # Serialise the message and send it.
            try:
                message_bytes = serialize(request)
            except ValueError as exc:
                print(f"[ERROR] {exc}")
                continue
            client_socket.sendto(message_bytes, (HOST, PORT))

            # Wait for a response.
            try:
                response_bytes, _ = client_socket.recvfrom(65535)
            except socket.timeout:
                print("[TIMEOUT] No reply within 5 s; UDP does not guarantee delivery.")
                continue
            try:
                response: ResponseMessage = deserialize(response_bytes)
                if not isinstance(response, ResponseMessage):
                    raise ValueError("Unexpected response type")
            except Exception as exc:
                print(f"[ERROR] Invalid response: {type(exc).__name__}")
                continue

            # Display the response.
            print(response)


if __name__ == "__main__":
    main()
