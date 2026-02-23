"""S02 – Template TCP client (student task)

This file contains a minimal interactive TCP client.

Students are expected to complete the TODO section inside `main()`.
"""

import socket
import time

HOST = "127.0.0.1"
PORT = 12345


def main():
    # Create an IPv4 TCP socket.
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        print(f"[INFO] Connecting to {HOST}:{PORT} ...")
        s.connect((HOST, PORT))
        print("[INFO] Connected.")

        # >>> STUDENT CODE STARTS HERE
        """
        TODO (student):

        1. Ask the user to enter messages from the keyboard
           in a loop (using input()).

        2. For each message:
           - If the user enters 'exit', break the loop.
           - Measure the time before and after sending and receiving
             the server response (use time.time()).
           - Send the message as bytes (use .encode('utf-8')).
           - Read the server response with recv(1024).

        3. For each round, print:
           - the message that was sent
           - the response that was received
           - the total round-trip time (RTT) in milliseconds.

        Hints:
        - Use a while True loop:
              while True:
                  data = input("Message (or 'exit' to quit): ")
        - Convert to bytes: data.encode('utf-8')
        - RTT (ms): (t_after - t_before) * 1000
        """

        # <<< STUDENT CODE ENDS HERE

    print("[INFO] Connection closed.")


if __name__ == "__main__":
    main()
