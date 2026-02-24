"""S02 – Template UDP client (student task)

This file contains an interactive UDP client.

Objective:
- send repeated messages to a UDP server
- measure an approximate RTT (application-level timing)
- print simple statistics (sent/received/loss)
"""

import socket
import sys
import time


def main():
    # Usage:
    #   python3 S02_Part10_Template_UDP_Client.py <HOST> <PORT>
    if len(sys.argv) < 3:
        print(f"Usage: {sys.argv[0]} <HOST> <PORT>")
        sys.exit(1)

    host = sys.argv[1]
    port = int(sys.argv[2])

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client_socket:
        print(f"[INFO] UDP client ready, sending to {host}:{port}")
        sent_count = 0
        received_count = 0

        # >>> STUDENT CODE STARTS HERE
        """
        TODO (student):

        1. Implement an interactive loop:
           - use while True:
               - read a message with input()
               - if the message is "exit", break

        2. For each message:
           - increment 'sent_count'
           - record the time before sendto(): t_before = time.time()
           - send the message to (host, port) encoded as UTF-8
           - set a socket timeout (e.g., 2 seconds) with:
                 client_socket.settimeout(2.0)
           - try to receive a reply with recvfrom(1024)
             * if you receive a reply:
                 - increment 'received_count'
                 - compute an approximate RTT: t_after - t_before
                 - print the reply and RTT in milliseconds
             * if you do not receive a reply (timeout):
                 - print a warning: "[WARN] No response (timeout)"

        3. After the loop ends ("exit"):
           - print a summary:
             * number of messages sent
             * number of replies received
             * loss percentage (if any)
        """
        # <<< STUDENT CODE ENDS HERE

        print("[INFO] UDP client terminated.")


if __name__ == "__main__":
    main()
