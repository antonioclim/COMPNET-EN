import socket
import struct
import time

MCAST_GRP = "224.0.0.1"
MCAST_PORT = 5001


def main():
    """
    UDP multicast receiver to be extended by the student.

    Objective:
    - display a timestamp for each message
    - count how many messages have been received
    """

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.bind(("", MCAST_PORT))

    group_bytes = socket.inet_aton(MCAST_GRP)
    mreq = struct.pack("4sL", group_bytes, socket.INADDR_ANY)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

    print(f"[INFO] UDP multicast receiver joined group {MCAST_GRP} on port {MCAST_PORT}")

    # >>> STUDENT CODE STARTS HERE
    """
    TODO (student):

    1. Initialise a counter = 0.

    2. In the while loop:
       - receive a message with recvfrom(1024)
       - increment counter
       - obtain the current time (time.time()) and convert it
         into a human-readable string (using time.strftime, time.localtime).

       - decode the message to UTF-8 text.

       - display a log of the form:
         [#<counter> at <timestamp>] From <ip>:<port> -> "<text>"

    3. Observe at runtime that multiple receivers running on
       different machines but in the same multicast group receive the same message.
       (This observation should be described in the output file.)
    """

    # <<< STUDENT CODE ENDS HERE


if __name__ == "__main__":
    main()
