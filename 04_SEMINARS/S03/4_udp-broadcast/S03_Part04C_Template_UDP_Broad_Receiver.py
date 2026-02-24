import socket

LISTEN_ADDR = ""
LISTEN_PORT = 5007


def main():
    """
    UDP broadcast receiver to be extended by the student.

    Objective:
    - count how many messages have been received
    - filter messages by a prefix
    """

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((LISTEN_ADDR, LISTEN_PORT))

    print(f"[INFO] UDP broadcast receiver listening on 0.0.0.0:{LISTEN_PORT}")

    # >>> STUDENT CODE STARTS HERE
    """
    TODO (student):

    1. Initialise a variable counter = 0 (before the while loop).
    2. In the infinite loop:
       - receive data with recvfrom(1024).
       - decode the message to UTF-8 text.
       - increment counter by 1.

       - If the message does NOT start with the prefix "Hello",
         display a log:
           [SKIP] From <ip>:<port> -> "<text>"
         and continue to the next message (continue).

       - If the message starts with "Hello":
         display:
           [OK] (#<counter>) From <ip>:<port> -> "<text>"

    Hints:
    - use text.startswith("Hello")
    - remember to display the current message count (counter)
    """

    # <<< STUDENT CODE ENDS HERE


if __name__ == "__main__":
    main()
