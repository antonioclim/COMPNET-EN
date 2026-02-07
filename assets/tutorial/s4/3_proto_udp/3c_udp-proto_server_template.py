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

state = State()


def main():
    """
    Server UDP pentru protocolul custom.

    TODO (student):
      - Adăugați suport pentru mesajul CLEAR:
        * RequestMessageType.CLEAR
        * Golește notițele clientului fără a-l deconecta.
    """

    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <PORT>")
        sys.exit(1)

    PORT = int(sys.argv[1])

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_socket:
        server_socket.bind(("", PORT))
        print(f"[INFO] UDP protocol server (template) listening on 0.0.0.0:{PORT}")

        while True:
            message_bytes, address = server_socket.recvfrom(1024)
            request = deserialize(message_bytes)

            print(f"[RECV] From {address} -> {request}")

            # >>> STUDENT CODE STARTS HERE
            """
            TODO (student):

            Implementați logica de server pentru tipurile de mesaje:

              1. CONNECT
                 - adăugați clientul în state.connections
                 - trimiteți ResponseMessage(OK)

              2. SEND
                 - dacă address este în state.connections:
                     * adăugați notița în state (state.add_note)
                     * trimiteți ResponseMessage(OK)
                   altfel:
                     * ResponseMessage(ERR_CONNECTED)

              3. LIST
                 - dacă address este în state.connections:
                     * trimiteți ResponseMessage(OK, <notițe>)
                   altfel:
                     * ResponseMessage(ERR_CONNECTED)

              4. DISCONNECT
                 - dacă address este în state.connections:
                     * eliminați clientul din state (state.remove_connection)
                     * ResponseMessage(OK)
                   altfel:
                     * ResponseMessage(ERR_CONNECTED)

              5. CLEAR (nou)
                 - dacă address este în state.connections:
                     * ștergeți notițele clientului (state.clear_notes)
                     * ResponseMessage(OK)
                   altfel:
                     * ResponseMessage(ERR_CONNECTED)

              6. orice alt tip:
                 - ResponseMessage(ERR_UNKNOWN)

            Nu uitați să serializați răspunsul cu serialize()
            și să îl trimiteți cu sendto(response_bytes, address).
            """

            # Exemplu de schelet (completați ramurile corespunzătoare):
            if request.message_type == RequestMessageType.CONNECT:
                # TODO: implement CONNECT
                response = ResponseMessage(ResponseMessageType.OK)

            elif request.message_type == RequestMessageType.SEND:
                # TODO: implement SEND (cu verificare de conexiune)
                response = ResponseMessage(ResponseMessageType.ERR_CONNECTED)

            elif request.message_type == RequestMessageType.LIST:
                # TODO: implement LIST
                response = ResponseMessage(ResponseMessageType.ERR_CONNECTED)

            elif request.message_type == RequestMessageType.DISCONNECT:
                # TODO: implement DISCONNECT
                response = ResponseMessage(ResponseMessageType.ERR_CONNECTED)

            elif request.message_type == RequestMessageType.CLEAR:
                # TODO: implement CLEAR
                response = ResponseMessage(ResponseMessageType.ERR_CONNECTED)

            else:
                response = ResponseMessage(ResponseMessageType.ERR_UNKNOWN, "Unknown request type")

            # Serializăm și trimitem răspunsul.
            response_bytes = serialize(response)
            server_socket.sendto(response_bytes, address)
            print(f"[SEND] To {address} -> {response}\n")
            # <<< STUDENT CODE ENDS HERE


if __name__ == "__main__":
    main()
