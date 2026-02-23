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

state = State()


def main():
    """
    UDP server for the custom protocol.

    TODO (student):
      - Add support for the CLEAR message:
        * RequestMessageType.CLEAR
        * Clears the client's notes without disconnecting.
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

            Implement the server logic for the following message types:

              1. CONNECT
                 - add the client to state.connections
                 - send ResponseMessage(OK)

              2. SEND
                 - if address is in state.connections:
                     * add the note to state (state.add_note)
                     * send ResponseMessage(OK)
                   otherwise:
                     * ResponseMessage(ERR_CONNECTED)

              3. LIST
                 - if address is in state.connections:
                     * send ResponseMessage(OK, <notes>)
                   otherwise:
                     * ResponseMessage(ERR_CONNECTED)

              4. DISCONNECT
                 - if address is in state.connections:
                     * remove the client from state (state.remove_connection)
                     * ResponseMessage(OK)
                   otherwise:
                     * ResponseMessage(ERR_CONNECTED)

              5. CLEAR (new)
                 - if address is in state.connections:
                     * clear the client's notes (state.clear_notes)
                     * ResponseMessage(OK)
                   otherwise:
                     * ResponseMessage(ERR_CONNECTED)

              6. any other type:
                 - ResponseMessage(ERR_UNKNOWN)

            Remember to serialise the response with serialize()
            and send it with sendto(response_bytes, address).
            """

            # Example skeleton (fill in the corresponding branches):
            if request.message_type == RequestMessageType.CONNECT:
                # TODO: implement CONNECT
                response = ResponseMessage(ResponseMessageType.OK)

            elif request.message_type == RequestMessageType.SEND:
                # TODO: implement SEND (with connection check)
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

            # Serialise and send the response.
            response_bytes = serialize(response)
            server_socket.sendto(response_bytes, address)
            print(f"[SEND] To {address} -> {response}\n")
            # <<< STUDENT CODE ENDS HERE


if __name__ == "__main__":
    main()
