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
    UDP client for the custom protocol.

    TODO (student):
      - Add the 'clear' command that sends RequestMessageType.CLEAR.
    """

    if len(sys.argv) < 3:
        print(f"Usage: {sys.argv[0]} <HOST> <PORT>")
        sys.exit(1)

    HOST, PORT = sys.argv[1:3]
    PORT = int(PORT)

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client_socket:
        client_socket.settimeout(5)
        print(f"[INFO] UDP client (template) sending to {HOST}:{PORT}")

        while True:
            data = input("storage> ").strip()

            if not data:
                continue

            if data == "exit":
                print("[INFO] Exiting client.")
                break

            items = data.split(" ", 1)
            command = items[0]

            # >>> STUDENT CODE STARTS HERE
            """
            TODO (student):

            1. Implement the following commands:

               - connect
                   RequestMessage(RequestMessageType.CONNECT)

               - send <text...>
                   RequestMessage(RequestMessageType.SEND, payload=<text>)

               - list
                   RequestMessage(RequestMessageType.LIST)

               - disconnect
                   RequestMessage(RequestMessageType.DISCONNECT)

               - clear
                   RequestMessage(RequestMessageType.CLEAR)

            2. If the command is not recognised, print:
               "[WARN] unknown command" and continue.

            3. After sending the request, receive a response with
               recvfrom(65535), deserialise it and print it.
            """

            # Example: minimal skeleton
            if command == "connect":
                request = RequestMessage(RequestMessageType.CONNECT)

            elif command == "send":
                if len(items) < 2:
                    print("[WARN] send requires a payload")
                    continue
                payload = items[1]
                request = RequestMessage(RequestMessageType.SEND, payload)

            elif command == "list":
                request = RequestMessage(RequestMessageType.LIST)

            elif command == "disconnect":
                request = RequestMessage(RequestMessageType.DISCONNECT)

            elif command == "clear":
                # TODO: implement CLEAR request
                request = RequestMessage(RequestMessageType.CLEAR)

            else:
                print("[WARN] unknown command")
                continue

            # Send the request and receive the response.
            try:
                message_bytes = serialize(request)
            except ValueError as exc:
                print(f"[ERROR] {exc}")
                continue
            client_socket.sendto(message_bytes, (HOST, PORT))

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
            print(response)
            # <<< STUDENT CODE ENDS HERE


if __name__ == "__main__":
    main()
