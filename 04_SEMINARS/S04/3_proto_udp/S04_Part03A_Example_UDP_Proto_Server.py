import socket
import sys

from S04_Part03_Script_Transfer_Units import (
    RequestMessage,
    RequestMessageType,
    ResponseMessage,
    ResponseMessageType,
)
from S04_Part03_Script_State import State
from S04_Part03_Script_Serialization import serialize, deserialize

# Global state instance.
state = State()


def main():
    """
    UDP server implementing a small protocol with message types.

    Protocol (conceptual level):

      Request types:
        - CONNECT
        - SEND <note>
        - LIST
        - DISCONNECT

      Response types:
        - OK
        - ERR_CONNECTED (if the client is not registered)
    """

    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <PORT>")
        sys.exit(1)

    PORT = int(sys.argv[1])

    # UDP socket (IPv4).
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_socket:
        server_socket.bind(("", PORT))
        print(f"[INFO] UDP protocol server listening on 0.0.0.0:{PORT}")

        while True:
            # recvfrom gives us (message_bytes, address).
            message_bytes, address = server_socket.recvfrom(1024)

            # Deserialise the RequestMessage from bytes.
            request: RequestMessage = deserialize(message_bytes)
            print(f"[RECV] From {address} -> {request}")

            # For each message type, apply logic on 'state'.
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
                # Unknown message type (should not occur in the example).
                response = ResponseMessage(ResponseMessageType.ERR_UNKNOWN)

            # Serialise and send the response.
            response_bytes = serialize(response)
            server_socket.sendto(response_bytes, address)
            print(f"[SEND] To {address} -> {response}\n")


if __name__ == "__main__":
    main()
