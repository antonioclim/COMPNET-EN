import socket
import sys

from transfer_units import (
    RequestMessage,
    RequestMessageType,
    ResponseMessage,
    ResponseMessageType,
)
from state import State
from serialization import serialize, deserialize

# Instanța globală de stare.
state = State()


def main():
    """
    Server UDP care implementează un mic protocol cu message types.

    Protocol (la nivel conceptual):

      Request types:
        - CONNECT
        - SEND <note>
        - LIST
        - DISCONNECT

      Response types:
        - OK
        - ERR_CONNECTED (dacă clientul nu este înregistrat)
    """

    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <PORT>")
        sys.exit(1)

    PORT = int(sys.argv[1])

    # Socket UDP (IPv4).
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_socket:
        server_socket.bind(("", PORT))
        print(f"[INFO] UDP protocol server listening on 0.0.0.0:{PORT}")

        while True:
            # Recvfrom ne dă (message_bytes, address).
            message_bytes, address = server_socket.recvfrom(1024)

            # Deserializăm RequestMessage din bytes.
            request: RequestMessage = deserialize(message_bytes)
            print(f"[RECV] From {address} -> {request}")

            # Pentru fiecare tip de mesaj, aplicăm logică pe 'state'.
            if request.message_type == RequestMessageType.CONNECT:
                state.add_connection(address)
                response = ResponseMessage(ResponseMessageType.OK)

            elif request.message_type == RequestMessageType.SEND:
                if address in state.connections:
                    state.add_note(address, request.payload)
                    response = ResponseMessage(ResponseMessageType.OK)
                else:
                    response = ResponseMessage(ResponseMessageType.ERR_CONNECTED)

            elif request.message_type == RequestMessageType.LIST:
                if address in state.connections:
                    notes = state.get_notes(address)
                    response = ResponseMessage(ResponseMessageType.OK, notes)
                else:
                    response = ResponseMessage(ResponseMessageType.ERR_CONNECTED)

            elif request.message_type == RequestMessageType.DISCONNECT:
                if address in state.connections:
                    state.remove_connection(address)
                    response = ResponseMessage(ResponseMessageType.OK)
                else:
                    response = ResponseMessage(ResponseMessageType.ERR_CONNECTED)

            else:
                # Tip de mesaj necunoscut (nu ar trebui să apară în exemplu).
                response = ResponseMessage(ResponseMessageType.ERR_UNKNOWN)

            # Serializăm și trimitem răspunsul.
            response_bytes = serialize(response)
            server_socket.sendto(response_bytes, address)
            print(f"[SEND] To {address} -> {response}\n")


if __name__ == "__main__":
    main()
