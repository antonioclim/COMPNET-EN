import socket

ANYCAST_ADDR = "::"
PORT = 5007


def anycast_server():
    """
    Simulated UDP IPv6 "anycast" server.

    Student objective:
    - add a "server_id" to the response (to see which server is replying)
    """

    sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
    sock.bind((ANYCAST_ADDR, PORT))

    # >>> STUDENT CODE STARTS HERE
    """
    TODO (student):

    1. Prompt the user to enter a "server_id"
       (e.g. "S1", "S2", etc.) using input().

    2. In the while loop:
       - receive a message with recvfrom(1024).
       - decode the message text.
       - display a log:
         [RECV-<server_id>] From <addr> -> "<text>"

       - construct a reply of the form:
         f"[{server_id}] Reply from anycast server"
         and send it back to the client (encoded as UTF-8).

       - display a log:
         [SEND-<server_id>] To <addr> -> "<reply>"
    """

    # <<< STUDENT CODE ENDS HERE


if __name__ == "__main__":
    anycast_server()
