import socket
import sys

from transfer_units import (
    RequestMessage,
    RequestMessageType,
    ResponseMessage,
    ResponseMessageType,
)
from serialization import serialize, deserialize


def main():
    """
    Client UDP pentru protocolul custom.

    TODO (student):
      - Adăugați comanda 'clear' care trimite RequestMessageType.CLEAR.
    """

    if len(sys.argv) < 3:
        print(f"Usage: {sys.argv[0]} <HOST> <PORT>")
        sys.exit(1)

    HOST, PORT = sys.argv[1:3]
    PORT = int(PORT)

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client_socket:
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

            1. Implementați următoarele comenzi:

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

            2. Dacă comanda nu este recunoscută, afișați:
               "[WARN] unknown command" și continuați.

            3. După trimiterea cererii, primiți un răspuns cu
               recvfrom(1024), deserializați-l și afișați-l.
            """

            # Exemplu: schelet minimal
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

            # Trimitem cererea și primim răspunsul.
            message_bytes = serialize(request)
            client_socket.sendto(message_bytes, (HOST, PORT))

            response_bytes, _ = client_socket.recvfrom(1024)
            response: ResponseMessage = deserialize(response_bytes)
            print(response)
            # <<< STUDENT CODE ENDS HERE


if __name__ == "__main__":
    main()
