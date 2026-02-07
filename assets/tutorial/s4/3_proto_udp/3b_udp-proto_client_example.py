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
    Client UDP interactiv pentru mini-protocol.

    Comenzi (la prompt-ul "storage>"):

      connect
      send <text...>
      list
      disconnect
      exit   (doar închide clientul, nu trimite nimic special)
    """

    if len(sys.argv) < 3:
        print(f"Usage: {sys.argv[0]} <HOST> <PORT>")
        sys.exit(1)

    HOST, PORT = sys.argv[1:3]
    PORT = int(PORT)

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client_socket:
        print(f"[INFO] UDP client ready, sending to {HOST}:{PORT}")

        while True:
            data = input("storage> ").strip()

            if not data:
                continue

            if data == "exit":
                print("[INFO] Exiting client.")
                break

            # Spargem comanda în maxim 2 bucăți: command + rest.
            items = data.split(" ", 1)
            command = items[0]

            # Construim RequestMessage în funcție de command.
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

            # Serializăm mesajul și îl trimitem.
            message_bytes = serialize(request)
            client_socket.sendto(message_bytes, (HOST, PORT))

            # Așteptăm un răspuns.
            response_bytes, _ = client_socket.recvfrom(1024)
            response: ResponseMessage = deserialize(response_bytes)

            # Afișăm răspunsul.
            print(response)


if __name__ == "__main__":
    main()
